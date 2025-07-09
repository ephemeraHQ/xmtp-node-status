from collections import defaultdict
import concurrent.futures
from flask import Flask, render_template_string
import grpc
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
import json
import os
import time
from web3 import Web3

addresses = {}
errors = defaultdict(str)
versions = defaultdict(str)
app = Flask(__name__)

def get_addresses():
    web3 = Web3(Web3.HTTPProvider(os.environ["WEB3_PROVIDER_URI"]))

    if not web3.is_connected():
        raise ConnectionError("Failed to connect to the network")

    # Contract address
    contract_address = "0x5275FfA7D1f5aBd4159Ae38925fD9F4D5686725E"

    with open("NodeRegistry.abi.json", "r") as abi_file:
        contract = json.load(abi_file)

    # Load the contract
    contract = web3.eth.contract(address=contract_address, abi=contract)

    result = contract.functions.getAllNodes().call()

    canonical_nodes = [
        node[1][3].replace("https://", "") + ":443"
        for node in result
        if node[1][1] is True and node[1][3]  # isCanonical and has httpAddress
    ]

    return canonical_nodes

def check_grpc_status(address):
    """
    Function to check if the gRPC endpoint is reachable
    by establishing a secure gRPC connection and calling the reflection API.
    """
    version = "no version detected"
    
    try:
        # Create a secure gRPC channel
        channel = grpc.secure_channel(address, grpc.ssl_channel_credentials())

        # Create a stub for reflection API
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        request = reflection_pb2.ServerReflectionRequest(list_services="")

        # Call the reflection API with timeout
        response_iterator = stub.ServerReflectionInfo(iter([request]), timeout=10)
        services = []
        
        for resp in response_iterator:
            if resp.HasField('list_services_response'):
                services.extend([service.name for service in resp.list_services_response.service])

        # If response is received, mark as reachable
        if services:
            errors[address] = ""  # Clear any previous errors
            version = get_service_version(services, channel)
            channel.close()
            return address, version, "✅ Reachable"

        else:
            errors[address] = "No response from server"
            channel.close()
            return address, version, "❌ No Response"

    except grpc.RpcError as e:
        error_message = f"gRPC Error: {e.code().name} - {str(e.details())}"
        errors[address] = error_message
        return address, version, f"❌ Error: {e.code().name}"

    except Exception as e:
        error_message = f"Exception: {str(e)}"
        errors[address] = error_message
        return address, version, "⚠️ Exception"

def get_service_version(services, channel):
    """
    Try to get version information from MetadataApi service
    """
    version = "no version detected"
    
    # Look for the MetadataApi service specifically
    metadata_service = None
    for service in services:
        if 'xmtp.xmtpv4.metadata_api.MetadataApi' in service:
            metadata_service = service
            break
    
    if not metadata_service:
        return version
    
    try:
        # Import the generated stubs
        import metadata_api_pb2 as metadata_api_pb2
        import metadata_api_pb2_grpc as metadata_api_pb2_grpc
        
        # Create the MetadataApi stub
        stub = metadata_api_pb2_grpc.MetadataApiStub(channel)
        
        # Create the GetVersion request
        request = metadata_api_pb2.GetVersionRequest()
        
        # Call GetVersion with a timeout
        response = stub.GetVersion(request, timeout=2)
        
        # Return the actual version string
        if response.version:
            return response.version
        else:
            return version
            
    except grpc.RpcError as e:
        return version
    except ImportError as e:
        return version
    except Exception as e:
        return version

def update_status():
    """
    Runs gRPC checks in parallel for all addresses using ThreadPoolExecutor
    and updates the list of addresses dynamically.
    """
    global addresses, errors
    while True:
        try:
            new_addresses = set(get_addresses())  # Fetch the latest node addresses

            # Identify added and removed addresses
            current_addresses = set(addresses.keys())
            added_addresses = new_addresses - current_addresses
            removed_addresses = current_addresses - new_addresses

            # Remove old addresses
            for addr in removed_addresses:
                addresses.pop(addr, None)
                errors.pop(addr, None)

            # Add new addresses with a default status
            for addr in added_addresses:
                addresses[addr] = "Checking..."

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_address = {executor.submit(check_grpc_status, addr): addr for addr in addresses.keys()}
                for future in concurrent.futures.as_completed(future_to_address):
                    address, version, status = future.result()
                    addresses[address] = status  # Update the dictionary with the new status
                    versions[address] = version

        except Exception as e:
            print(f"Error updating status: {e}")  # Log errors if any

        time.sleep(10)  # Refresh every 10 seconds

# Start gRPC checking in a separate thread
import threading

threading.Thread(target=update_status, daemon=True).start()

@app.route("/data")
def data():
    return {"addresses": addresses, "versions": versions, "errors": errors}
@app.route("/")
def index():
    return render_template_string("""
        <html>
        <head>
            <title>XMTP Node Status</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #f9f9f9; }
                table { margin: auto; border-collapse: collapse; width: 70%; background: white; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #007bff; color: white; cursor: pointer; }
                .error-tooltip {
                    text-decoration: underline;
                    cursor: help;
                    color: red;
                }
            </style>
            <script>
                function refreshData() {
                    fetch('/data')  // Fetch updated data from the server
                        .then(response => response.json())
                        .then(data => {
                            let tableBody = document.getElementById("status-table-body");
                            tableBody.innerHTML = ""; // Clear existing rows

                            Object.keys(data.addresses).sort().forEach(addr => {
                                let row = tableBody.insertRow();
                                let cell1 = row.insertCell(0);
                                let cell2 = row.insertCell(1);
                                let cell3 = row.insertCell(2);

                                cell1.textContent = addr;
                                cell2.textContent = data.versions[addr];
                                if (data.addresses[addr].includes("Error") || data.addresses[addr].includes("Exception")) {
                                    cell3.innerHTML = `<span class="error-tooltip" title="${data.errors[addr]}">${data.addresses[addr]}</span>`;
                                } else {
                                    cell3.textContent = data.addresses[addr];
                                }
                            });
                        })
                        .catch(error => console.error("Error fetching data:", error));
                }

                setInterval(refreshData, 1000);  // Refresh every second without page reload
                window.onload = refreshData;  // Load data on page load
            </script>
        </head>
<body>
            <h1>XMTP Node Status</h1>
            <p>Data refreshes every second</p>
            <table>
                <thead>
                    <tr>
                        <th>Node Address</th>
                        <th>Version</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="status-table-body">
                    {% for addr, status in addresses.items() %}
                    <tr>
                        <td>{{ addr }}</td>
                        <td>{{ versions[addr] }}</td>
                        <td>
                            {% if "Error" in status or "Exception" in status %}
                                <span class="error-tooltip" title="{{ errors[addr] }}">{{ status }}</span>
                            {% else %}
                                {{ status }}
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
    """, addresses=addresses, versions=versions, errors=errors)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Accessible from local network

from flask import Flask, render_template_string
import grpc
import concurrent.futures
import time
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc

# JSON input (List of gRPC nodes)
JSON_DATA = [
    {"NodeID": 101, "HttpAddress": "https://grpc.testnet.xmtp.network"},
    {"NodeID": 200, "HttpAddress": "https://grpc2.testnet.xmtp.network"},
    {"NodeID": 400, "HttpAddress": "https://xmtp.nextnext.id"},
    {"NodeID": 500, "HttpAddress": "https://grpc.ens-xmtp.com"},
    {"NodeID": 600, "HttpAddress": "https://xmtp.validators.laminatedlabs.net"},
    {"NodeID": 700, "HttpAddress": "https://xmtp.artifact.systems"}
]

# Extract and format addresses (remove HTTPS, add :443)
addresses = {entry["HttpAddress"].replace("https://", "") + ":443": "Checking..." for entry in JSON_DATA}
errors = {address: "" for address in addresses}  # Store additional error details

app = Flask(__name__)


def check_grpc_status(address):
    """
    Function to check if the gRPC endpoint is reachable
    by establishing a secure gRPC connection and calling the reflection API.
    """
    try:
        # Create a secure gRPC channel
        channel = grpc.secure_channel(address, grpc.ssl_channel_credentials())

        # Create a stub for reflection API
        stub = reflection_pb2_grpc.ServerReflectionStub(channel)
        request = reflection_pb2.ServerReflectionRequest(list_services="")

        # Call the reflection API
        response_iterator = stub.ServerReflectionInfo(iter([request]))
        services = [resp.list_services_response for resp in response_iterator]

        # If response is received, mark as reachable
        if services:
            errors[address] = ""  # Clear any previous errors
            return address, "✅ Reachable"
        else:
            errors[address] = "No response from server"
            return address, "❌ No Response"

    except grpc.RpcError as e:
        error_message = f"gRPC Error: {e.code().name} - {str(e.details())}"
        errors[address] = error_message
        return address, f"❌ Error: {e.code().name}"

    except Exception as e:
        error_message = f"Exception: {str(e)}"
        errors[address] = error_message
        return address, "⚠️ Exception"


def update_status():
    """
    Runs gRPC checks in parallel for all addresses using ThreadPoolExecutor.
    """
    global addresses
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_address = {executor.submit(check_grpc_status, addr): addr for addr in addresses.keys()}
            for future in concurrent.futures.as_completed(future_to_address):
                address, status = future.result()
                addresses[address] = status  # Update the dictionary with the new status

        time.sleep(10)  # Refresh every 10 seconds


# Start gRPC checking in a separate thread
import threading

threading.Thread(target=update_status, daemon=True).start()


# Flask Web Route
@app.route("/")
def index():
    return render_template_string("""
        <html>
        <head>
            <title>XMTP Node Status</title>
            <meta http-equiv="refresh" content="1">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #f9f9f9; }
                table { margin: auto; border-collapse: collapse; width: 70%; background: white; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #007bff; color: white; }
                .error-tooltip {
                    text-decoration: underline;
                    cursor: help;
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>XMTP Node Status</h1>
            <p>Page refreshes every second</p>
            <table>
                <tr><th>Node Address</th><th>Status</th></tr>
                {% for addr, status in addresses.items() %}
                <tr>
                    <td>{{ addr }}</td>
                    <td>
                        {% if "Error" in status or "Exception" in status %}
                            <span class="error-tooltip" title="{{ errors[addr] }}">{{ status }}</span>
                        {% else %}
                            {{ status }}
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
    """, addresses=addresses, errors=errors)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Accessible from local network

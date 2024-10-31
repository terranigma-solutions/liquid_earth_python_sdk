import socket
import os

from dotenv import load_dotenv

load_dotenv()

def make_url(endpoint: str) -> str:
    return f"{BASE_URL}/{endpoint}"

backend_override = os.environ.get("BACKEND_OVERRIDE")
# If backend_override is local host, use the socket.gethostname() to get the local host name
if "localhost" in backend_override:
    port = backend_override.split(":")[-1].split("/")[0]
    backend_override = f"http://{socket.gethostname()}.local:{port}/api"


BASE_URL =  f"https://apim-liquidearth.azure-api.net/python" if backend_override is None else backend_override
    


def handle_response(response) -> any:
    """ Helper function to handle common response logic. """
    if response.ok:
        content_type_ = response.headers['Content-Type']
        parsed_response = response.json() if 'application/json' in content_type_ else response.text
        return parsed_response
    else:
        raise ValueError(f"HTTP Error {response.status_code}: {response.reason} {response.text}")

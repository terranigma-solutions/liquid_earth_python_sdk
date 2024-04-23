import socket


def make_url(endpoint: str) -> str:
    return f"{BASE_URL}/{endpoint}"


LOCAL = True  # Set to True for local development, False for server
BASE_URL = f"https://apim-liquidearth.azure-api.net/python" if not LOCAL else\
    f"http://{socket.gethostname()}.local:7071/api"


def handle_response(response) -> dict:
    """ Helper function to handle common response logic. """
    if response.ok:
        return response.json() if response.headers['Content-Type'] == 'application/json' else response.text
    else:
        raise ValueError(f"HTTP Error {response.status_code}: {response.reason} {response.text}")

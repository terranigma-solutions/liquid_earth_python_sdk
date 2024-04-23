import socket


def make_url(endpoint: str) -> str:
    return f"{BASE_URL}/{endpoint}"


LOCAL = True  # Set to True for local development, False for server
BASE_URL = f"https://apim-liquidearth.azure-api.net/python" if not LOCAL else\
    f"http://{socket.gethostname()}.local:7071/api"


def handle_response(response) -> any:
    """ Helper function to handle common response logic. """
    if response.ok:
        content_type_ = response.headers['Content-Type']
        parsed_response = response.json() if 'application/json' in content_type_ else response.text
        return parsed_response
    else:
        raise ValueError(f"HTTP Error {response.status_code}: {response.reason} {response.text}")

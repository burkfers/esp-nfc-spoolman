try:
    import ujson as json
except ImportError:
    json = None
import socket
import requests
from config import MOONRAKER_HOST, MOONRAKER_PORT

def set_next_spoolid(spool_id):
    """Send a POST request to http://<host>/api/printer/command with a test command using requests."""
    url = 'http://{}:{}/api/printer/command'.format(MOONRAKER_HOST, MOONRAKER_PORT)
    # Use a list of strings, not f-strings, to avoid extra memory use
    commands = []
    commands.append("MMU_GATE_MAP NEXT_SPOOLID=" + str(spool_id))
    commands.append("M118 Next Spool ID is " + str(spool_id))
    payload = {"commands": commands}
    try:
        resp = requests.post(url, json=payload)
        print("Printer POST response:", resp.status_code, resp.text)
    except requests.ConnectionError as e:
        print("POST failed: Connection error:", e)
    except requests.Timeout as e:
        print("POST failed: Timeout:", e)
    except requests.RequestException as e:
        print("POST failed: Request exception:", e)
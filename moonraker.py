try:
    import ujson as json
except ImportError:
    json = None
import socket
import requests
from config import MOONRAKER_HOST, MOONRAKER_PORT, USE_NEXT_SPOOLID

def get_current_gate():
    url = 'http://{}:{}/printer/objects/query?mmu=gate'.format(MOONRAKER_HOST, MOONRAKER_PORT)
    try:
        resp = requests.get(url)
        print("Printer GET response:", resp.status_code, resp.text)
        return resp.json()['result']['status']['mmu']['gate']
    except requests.ConnectionError as e:
        print("GET failed: Connection error:", e)
    except requests.Timeout as e:
        print("GET failed: Timeout:", e)
    except requests.RequestException as e:
        print("GET failed: Request exception:", e)
    return -1


def set_next_spoolid(spool_id):
    """Send a POST request to http://<host>/api/printer/command with a test command using requests."""
    url = 'http://{}:{}/api/printer/command'.format(MOONRAKER_HOST, MOONRAKER_PORT)
    # Use a list of strings, not f-strings, to avoid extra memory use
    commands = []
    if USE_NEXT_SPOOLID:
        commands.append("MMU_GATE_MAP NEXT_SPOOLID=" + str(spool_id))
        commands.append("M118 Next Spool ID is " + str(spool_id))
    else:
        gate = get_current_gate()
        commands.append("MMU_GATE_MAP GATE={} SPOOLID={}".format(gate, spool_id))
        commands.append("M118 Gate {} Spool ID is {}".format(gate, spool_id))
    payload = {"commands": commands}
    try:
        resp = requests.post(url, json=payload)
        print("Printer POST response:", resp.status_code, resp.text)
        return resp.status_code == 200
    except requests.ConnectionError as e:
        print("POST failed: Connection error:", e)
    except requests.Timeout as e:
        print("POST failed: Timeout:", e)
    except requests.RequestException as e:
        print("POST failed: Request exception:", e)
    return False

import base64
import json
import ssl
import time
from time import sleep
import websocket
from wakeonlan import send_magic_packet



class SamsungTV:
    def __init__(self, ip: str, token: str | None = None, mac_address: str | None = None):
        self.ip = ip
        self.ws = None
        self.token = token
        self.mac = mac_address  # Replace with your Samsung TV's MAC address

    def connect(self):
        name = base64.b64encode(
            b"Jarvis"
        ).decode("utf-8")

        url = (
            f"wss://{self.ip}:8002/"
            f"api/v2/channels/samsung.remote.control"
            f"?name={name}"
        )

        if self.token:
            url += f"&token={self.token}"

        self.ws = websocket.create_connection(
            url,
            sslopt={"cert_reqs": ssl.CERT_NONE},
        )
        print("Token:", self.token)
        print("URL:", url)

        while True:
            response = json.loads(self.ws.recv())
            print(response)

            if response.get("event") == "ms.channel.connect":
                data = response.get("data", {})

                if "token" in data:
                    self.token = data["token"]

                break

    def send_key(self, key: str):
        payload = {
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey",
            },
        }

        self.ws.send(json.dumps(payload))

    def volume_up(self, steps: int = 1):
        for _ in range(steps):
            self.send_key("KEY_VOLUP")
            time.sleep(0.5)

    def volume_down(self, steps: int = 1):
        for _ in range(steps):
            self.send_key("KEY_VOLDOWN")
            time.sleep(0.5)

    def mute(self):
        self.send_key("KEY_MUTE")

    def home(self):
        self.send_key("KEY_HOME")

    def power_off(self):
        self.send_key("KEY_POWER")

    def power_on(self):
        # Try waking TV directly
        
            send_magic_packet(
            self.mac,
            ip_address=self.ip,
            port=9,
    )

    
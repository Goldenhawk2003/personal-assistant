import requests


class UniluxThermostat:
    def __init__(self, ip: str):
        self.base_url = f"http://{ip}"

    def get_info(self):
        response = requests.get(
            self.base_url,
            timeout=5,
        )
        response.raise_for_status()

        return response.json()

    def get_status(self):
        response = requests.get(
            f"{self.base_url}/status",
            timeout=5,
        )
        response.raise_for_status()

        return response.json()
    def set_temperature(self, temperature: float):
        response = requests.post(
            f"{self.base_url}/set_temperature",
            json={"temperature": temperature},
            timeout=5,
        )
        response.raise_for_status()

        return response.json()

    def request(
        self,
        method: str,
        path: str = "/",
        **kwargs,
    ):
        url = f"{self.base_url}{path}"

        response = requests.request(
            method=method,
            url=url,
            timeout=5,
            **kwargs,
        )

        print("URL:", url)
        print("Status:", response.status_code)
        print("Headers:", dict(response.headers))
        print("Body:", response.text)

        return response
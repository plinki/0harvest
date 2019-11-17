import requests


class IP:
    def __init__(self, address=None, access_token=None):
        self.address = get()["ip"] if address is None else address
        self.loc = None
        self.hostname = None
        self.city = None
        self.region = None
        self.country = None
        self.org = None
        self.timezone = None
        self.tor = None

    def __repr__(self):
        return f"IP({self.address})"

    def __len__(self):
        return int(len(str("".join(list(filter(str.isdigit, self.address))))))

    def get(self, address=None):
        address = "" if address is None else address + "/"
        from harvest.fetcher import Fetcher
        _headers = {"authorization": f"Bearer {Fetcher.access_token}"}
        _headers = _headers if Fetcher.access_token else {}
        response = requests.get(
            f"http://ipinfo.io/{address}json", headers=_headers)

        return response.json()

    def populate(self):
        data = self.get(self.address)

        for key in [key for key in dir(self) if not key.startswith("__")]:
            if key in data and data[key] is not "":
                setattr(self, str(key), data[key])

        else:
            return True

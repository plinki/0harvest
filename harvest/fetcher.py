import re
import os
import requests
from harvest.ip import IP


class Fetcher:
    access_token = None

    def __init__(self, log_dir, _access_token=None):
        self.log_dir = log_dir
        self.fetched = []
        self.rgx = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        self.ignore = ["127.0.0.1"]
        self.fetch()

        Fetcher.access_token = _access_token

    def fetch(self):
        self._fetch_node_list()
        fetched_ips = [item.address for item in self.fetched]

        for file in os.listdir(self.log_dir):
            with open(f"{self.log_dir}{file}", "r") as file:
                for line in file:
                    address = self.rgx.findall(line)

                    for ip in address:
                        if ip not in self.ignore and ip not in fetched_ips:
                            _ip = IP(ip)
                            setattr(_ip, "tor", self._check_tor(_ip))
                            self.ignore.append(ip)
                            self.fetched.append(_ip)

        else:
            return self.fetched

    def _fetch_node_list(self):
        if not os.path.isfile("nodes"):
            req = requests.get("https://check.torproject.org/exit-addresses")
            req_lines = req.text.split("\n")

            with open("nodes", "w") as nodes_file:
                for line in req_lines:
                    if line.startswith("ExitAddress"):
                        ip = line.split(" ")[1]
                        nodes_file.write(f"{ip}\n")
                else:
                    return True

    def _check_tor(self, ip: IP):
        with open("nodes", "r") as nodes_file:
            if ip.address in nodes_file.read():
                return True

        return False

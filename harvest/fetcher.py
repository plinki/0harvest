import re
from harvest.ip import IP


class Fetcher:
    access_token = None

    def __init__(self, log_file, _access_token=None):
        self.log_file = log_file
        self.fetched = []
        self.rgx = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        self.ignore = ["127.0.0.1"]
        self.fetch()

        Fetcher.access_token = _access_token

    def fetch(self):
        fetched_ips = [item.address for item in self.fetched]
        with open(self.log_file, "r") as file:
            for line in file:
                address = self.rgx.findall(line)
                for ip in address:
                    if ip not in self.ignore and ip not in fetched_ips:
                        self.ignore.append(ip)
                        self.fetched.append(IP(ip))

            else:
                return self.fetched

#!/usr/bin/env python3.6

import argparse
from tqdm import tqdm
from harvest.ip import IP
from harvest.fetcher import Fetcher

parser = argparse.ArgumentParser(
    usage="cli.py log_directory --write filename [attributes]")
parser.add_argument("path", type=str,
                    help="The path to your log directory")
parser.add_argument("-w", "--write", type=str, metavar=("path", "attribute"), nargs="+",
                    help="Write output to path")
args = parser.parse_args()

harvester = Fetcher(args.path)

with open("config", "r") as config_file:
    for line in config_file:
        key, value = line.strip().split(":")
        if "token" in key and value is not "":
            harvester = Fetcher(args.path, value)


for ip in tqdm(harvester.fetched, leave=False, ascii=True):
    ip.populate()


def print_addresses(harvester: Fetcher):
    for ip in harvester.fetched:
        print(f"""
                IP: {ip.address}
                Location: {ip.loc}
                Hostname: {ip.hostname}
                City: {ip.city}
                Region: {ip.region}
                Country: {ip.country}
                Organization: {ip.org}
                Timezone: {ip.timezone}
                Tor: {ip.tor}
                """)
    print(f"Amount: {len(harvester.fetched)}")


def write(args_list):
    with open(args.write[0], "w") as file:
        for ip in harvester.fetched:
            for key in args_list[1:]:
                file.write(
                    f"{key}: {getattr(ip, key)}\n") if hasattr(ip, key) else None
                if key is args_list[-1]:
                    file.write("-"*30+"\n")


def main():
    print_addresses(harvester)
    if args.write:
        write(args.write)


if __name__ == "__main__":
    main()

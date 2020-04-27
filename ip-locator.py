# api url: http://api.ipstack.com/
# api key: a7b7a792adfc2bb96bb639263eadf0d5
# api use: http://api.ipstack.com/102.78.114.14?access_key=a7b7a792adfc2bb96bb639263eadf0d5&format=1


# import libraries:
import json, sys, os, re, argparse, platform
import requests as req
from datetime import datetime
from prettytable import PrettyTable

# Api info:
api_url = "http://api.ipstack.com/{}"
api_key = "a7b7a792adfc2bb96bb639263eadf0d5"

# banner:
banner = """
Author: Ismail Aatif @CyberLiberty | Version: 1.0
_________ _______    _        _______  _______  _______ _________ _______  _______ 
\__   __/(  ____ )  ( \      (  ___  )(  ____ \(  ___  )\__   __/(  ___  )(  ____ )
   ) (   | (    )|  | (      | (   ) || (    \/| (   ) |   ) (   | (   ) || (    )|
   | |   | (____)|  | |      | |   | || |      | (___) |   | |   | |   | || (____)|
   | |   |  _____)  | |      | |   | || |      |  ___  |   | |   | |   | ||     __)
   | |   | (        | |      | |   | || |      | (   ) |   | |   | |   | || (\ (   
___) (___| )        | (____/\| (___) || (____/\| )   ( |   | |   | (___) || ) \ \__
\_______/|/         (_______/(_______)(_______/|/     \|   )_(   (_______)|/   \__/
                                                                                   
"""
print(banner)

# handle arguments:
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", dest="address", help="IP Address to Look up.")
parser.add_argument("-f", "--file", dest="file", help="File Containing IP Addresses.")
args = parser.parse_args()


# check ip and request data:
def check_and_send(ip):
    _ip_ = re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", ip, re.I)
    if _ip_ != None:
        apiUrl = api_url.format(_ip_.group(0))
        response = req.get(
            url=apiUrl,
            params={"access_key": api_key, "format": 1},
            headers={},
            proxies={},
        )
        return response
    else:
        print("[!] IP Address Is Not Valid")
        sys.exit(0)


# clean terminal:
def clean():
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except Exception as e:
        print("[!] Problem Detected!")
        sys.exit(0)


def main(ip, mode, save2file):
    clean()
    print(banner)
    print("\nIP Location API @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 37)
    try:
        if mode == 1:
            # single ip check:
            response = check_and_send(ip=ip)
            if (response).status_code == 200:
                data = response.json()
                # printing information:
                print("[+] IP Address : {}".format(data["ip"]))
                print("[+] Continent  : {}".format(data["continent_name"]))
                print("[+] Country    : {}".format(data["country_name"]))
                print("[+] Region     : {}".format(data["region_name"]))
                print("[+] City       : {}".format(data["city"]))
                print("[+] Phone Code : {}".format(data["location"]["calling_code"]))
                print(
                    "[+] Language   : {}".format(
                        data["location"]["languages"][0]["name"]
                    )
                )
                print("[+] Flag       : {}".format(data["location"]["country_flag"]))
        else:
            # multiple ip check:
            with open(args.file, "r") as ip_list:
                newTabele = PrettyTable()
                newTabele.field_names = [
                    "IP Address",
                    "Continent",
                    "Country",
                    "Region",
                    "City",
                    "Phone Code",
                    "Langauge",
                    "Flag",
                ]
                for ip in ip_list.read().splitlines():
                    response = check_and_send(ip)
                    if (response).status_code == 200:
                        data = response.json()
                        # print information:
                        newTabele.add_row(
                            [
                                data["ip"],
                                data["continent_name"],
                                data["country_name"],
                                data["region_name"],
                                data["city"],
                                data["location"]["calling_code"],
                                data["location"]["languages"][0]["name"],
                                data["location"]["country_flag"],
                            ]
                        )
                print(newTabele)

    except KeyboardInterrupt:
        print("[CTRL-C] Detected.")
        sys.exit(0)


if __name__ == "__main__":
    if args.address is None and args.file is None:
        print("Use: ip-locator.py -h")
    else:
        if args.address != None:
            main(ip=args.address, mode=1, save2file=False)
        elif args.file != None:
            main(ip=args.address, mode=2, save2file=False)

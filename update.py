## Multitool auto updater
## This file will look for updates and if there is any it will automatically install it.
## Please avoid changing anything in this file.
APP_VERSION = "1.0.4"
APP_NAME = "Discord MultiTool"

import httpx
from colorama import Fore,Style
BASE_URL = "https://multitool.shahzain.me"
def lookforupdates():
    req = httpx.post(f"{BASE_URL}/api/update", json={
        "v": APP_VERSION
    }).json()
    if req["current"] == True:
        print(f"{Fore.GREEN}{Style.BRIGHT}You are up to date!{Style.RESET_ALL}")
    else:
        CURRENT_VERSION = req["version"]
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}You are not up to date.{Style.RESET_ALL}")
        choice = input(f"Do you wish to install MultiTool Version: {CURRENT_VERSION}? This will reset all your configuration files (y/n). \n>> ").lower()
        if choice == "n":
            return None
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/main.py")
        open("main.py", 'w').write(req.text)
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/massdm.py").text
        open("massdm.py", 'w').write(req)
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/utils.py").text
        open("utils.py", 'w').write(req)
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/memberscrapper.py").text
        open("memberscrapper.py", 'w').write(req)
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/message.json").text
        open("message.json", 'w').write(req)
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/config.json").text
        open("config.json", 'w').write(req)
        req = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/update.py").text
        open("update.py", 'w').write(req)
        print(f"{Fore.GREEN}{Style.BRIGHT}Installed MultiTool version {CURRENT_VERSION}\nPlease restart the tool.{Style.RESET_ALL}")
        exit()
lookforupdates()
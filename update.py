# Multitool auto updater
# This file will look for updates and if there is any it will automatically install it.
# Please avoid changing anything in this file.
from colorama import Fore, Style
import httpx
from src import getVersion
APP_VERSION = getVersion()
APP_NAME = "Discord MultiTool V2"

BASE_URL = "http://localhost:3001"


def lookforupdates():
    req = httpx.post(f"{BASE_URL}/api/v2/update", json={
        "v": APP_VERSION
    }, timeout=30).json()
    if req["current"] == True:
        print(f"{Fore.GREEN}{Style.BRIGHT}You are up to date!{Style.RESET_ALL}")
        if "message" in req:
            print(
                f"{Fore.YELLOW}{Style.BRIGHT}The api returned a message as well while looking for updates: \n{Style.RESET_ALL}{Style.BRIGHT}{Fore.GREEN}{req['message']}{Style.RESET_ALL}\n")
    else:
        try:
            CURRENT_VERSION = req["version"]
            print(
                f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}You are not up to date.{Style.RESET_ALL}")
            if "message" in req:
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}The api returned a message as well while looking for updates: \n{Style.RESET_ALL}{Style.BRIGHT}{Fore.GREEN}{req['message']}{Style.RESET_ALL}\n")
            choice = input(
                f"Do you wish to install MultiTool Version: {CURRENT_VERSION}? This will reset all your configuration files (y/n). \n>> ").lower()
            if choice != "y":
                return None
            client = httpx.Client()
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/main.py")
            open("main.py", 'w', encoding="utf-8").write(req.text)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/src/multitool.py").text
            open("src/multitool.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/src/scrapper.py").text
            open("src/scrapper.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/src/__init__.py").text
            open("src/__init__.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/src/_captcha.py").text
            open("src/_captcha.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/src/_utility.py").text
            open("src/_utility.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/src/global_variables.py").text
            open("src/global_variables.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/config.json").text
            open("config.json", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/update.py").text
            open("update.py", 'w', encoding="utf-8").write(req)
            req = client.get(
                "https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/messages.json").text
            open("messages.json", 'w', encoding="utf-8").write(req)
            print(f"{Fore.GREEN}{Style.BRIGHT}Installed MultiTool version {CURRENT_VERSION}\nPlease restart the tool.{Style.RESET_ALL}")
            exit()
        except:
            print(
                f"{Fore.RED}Failed to install update, please install it manually.{Style.RESET_ALL}")

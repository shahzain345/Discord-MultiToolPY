import random, json, re
from httpx import Client
from colorama import Fore, Style
from base64 import b64encode as b
import httpx
class Utility:
    def __init__(self):
        self.config = self.getConfig()
        self.proxy = self.getProxy()
    def getConfig(self):
        return json.loads(open("config.json").read())
    def getProxy(self):
        if self.config["proxy"]["proxyless"]:
            return None
        return f"{self.config['proxy']['protocol']}://{random.choice(open('input/proxies.txt').read().splitlines())}"
    def getBuildNum(self):
        """Gets the build number that discord is currently on, makes the x-super-properties header more realistic."""
        client = Client()
        asset = re.compile(r'([a-zA-z0-9]+)\.js', re.I).findall(client.get(f'https://discord.com/app', headers={'User-Agent': 'Mozilla/5.0'}).read().decode('utf-8'))[-1]
        fr = client.get(f'https://discord.com/assets/{asset}.js', headers={'User-Agent': 'Mozilla/5.0'}).read().decode('utf-8')
        return str(re.compile('Build Number: [0-9]+, Version Hash: [A-Za-z0-9]+').findall(fr)[0].replace(' ', '').split(',')[0].split(':')[-1]).replace(' ', '')
    def getContextProperties(self, guildId: str, channelId: str) -> str:
        return b(json.dumps({"location":"Join Guild","location_guild_id":guildId,"location_channel_id":channelId,"location_channel_type":0}, separators=(',', ':')).encode()).decode()
    def getInviteInfo(self, rawInvite):
        res = httpx.get(f'https://discord.com/api/v9/invites/{rawInvite}?with_counts=true', headers={
                             "Authorization": "undefined"}, timeout=30).json()
        return res

class MPrint:
    def w_print(self, message: str):
        """Print warning"""
        print(f"[{Style.BRIGHT}{Fore.RED}WARN{Style.RESET_ALL}] {Style.BRIGHT}{Fore.YELLOW}{message}{Style.RESET_ALL}")
    def s_print(self, message: str):
        """Print SUCCESS"""
        print(f"[{Style.BRIGHT}{Fore.MAGENTA}SUCCESS{Style.RESET_ALL}] {Style.BRIGHT}{Fore.GREEN}{message}{Style.RESET_ALL}")
    def f_print(self, message: str):
        """Print FAIL"""
        print(f"[{Style.BRIGHT}{Fore.YELLOW}FAILED{Style.RESET_ALL}] {Style.BRIGHT}{Fore.RED}{message}{Style.RESET_ALL}")
console = MPrint()
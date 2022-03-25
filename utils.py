from threading import Thread
from colorama import Fore, Style
from memberscrapper import MemberScrapper
from httpx import Client
from random import choice
from massdm import MassDM
from itertools import cycle
from globalvariables import qurantinedTokens
from json import load, dumps
from base64 import b64encode as b


def showMenu():
    print(f'{Style.BRIGHT}{Fore.YELLOW}1: Check Tokens {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}2: Join Server {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}3: Online Tokens {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.YELLOW}4: Format changer [Email:Pass:Token] => [Token] {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}5: Mass DM {Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}6: Single DM Spam {Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.YELLOW}7: Username Changer (Username list required(input/usernames.txt)) [Email:Pass:Token]{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}8: Scrape Members{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}9: Scrape Usernames{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}10: Server Leaver{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}11: Token Server Checker{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}12: Server spammer{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}13: Credits{Style.RESET_ALL}')
    print(
        f'{Style.BRIGHT}{Fore.YELLOW}14: Bio Changer (Bio list required(input/bios.txt)) [Token]{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}15: Reaction adder{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}16: Show configuration{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}17: Exit{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.YELLOW}18: Restart{Style.RESET_ALL}')


def scrapeMassMention(token, guildId, channelId):
    o = MassDM(token)
    res = o.getGuild(guildId)
    if "name" not in res:
        print(f"{token} is not in {guildId}")
        o.client.close()  # closes the session.
        return scrapeMassMention(choice(open("input/tokens.txt").read().splitlines()), guildId, channelId)
    scrapper = MemberScrapper(token=token)
    members = scrapper.get_members(guildId, channelId)
    data = []
    total_scraped = 0
    for memberID in members:
        if memberID not in data:
            total_scraped += 1
            data.append(int(memberID))
            print(f"{total_scraped}/{len(members)} - {memberID}")
    open("scraped/massmention.txt", "w").write("")
    with open("scraped/massmention.txt", "a") as fp:
        for userId in data:
            fp.write(str(userId) + "\n")
    guildName = o.getGuild(guildId)["name"] if 'name' in o.getGuild(
        guildId) else guildId
    print(f"{Fore.GREEN}{Style.BRIGHT}Successfully scrapped {len(data)} members in {guildName}{Style.RESET_ALL}")
    return True

def getInviteInfo(rawInvite):
    config = load(open('config.json'))
    if config["proxyless"] == True:
        with Client() as client:
            res = client.get(f'https://discord.com/api/v9/invites/{rawInvite}?with_counts=true', headers={
                             "Authorization": "undefined"}, timeout=config["request_timeout"]).json()
            return res
    else:
        with Client(proxies=f"http://{choice(open('input/proxies.txt').read().splitlines())}") as client:
            res = client.get(f'https://discord.com/api/v9/invites/{rawInvite}?with_counts=true', headers={
                             "Authorization": "undefined"}, timeout=config["request_timeout"]).json()
            return res


def getGoodToken():
    """Returns a token that is not qurantined, also websockets it"""
    tokens = open("input/tokens.txt").read().splitlines()
    c = load(open("config.json"))
    while True:
        token = choice(tokens)
        Thread(target=MassDM(token).websocketToken, daemon=True).start() if c["online_before_dm"] != False else None
        if token in qurantinedTokens:
            continue
        return token


def scrapeMembers(token, guildId, channelId):
    o = MassDM(token)
    res = o.getGuild(guildId)
    if "name" not in res:
        print(f"{token} is not in {guildId}")
        o.client.close()  # closes the session.
        return scrapeMembers(choice(open("input/tokens.txt").read().splitlines()), guildId, channelId)
    scrapper = MemberScrapper(token=token)
    members = scrapper.get_members(guildId, channelId)
    data = []
    total_scraped = 0
    for memberID in members:
        if memberID not in data:
            total_scraped += 1
            data.append(int(memberID))
            print(f"{total_scraped}/{len(members)} - {memberID}")
    open("scraped/members.txt", "w").write("")
    with open("scraped/members.txt", "a") as fp:
        for userId in data:
            fp.write(str(userId) + "\n")
    o = MassDM(token)
    guildName = o.getGuild(guildId)["name"]
    print(f"{Fore.GREEN}{Style.BRIGHT}Successfully scrapped {len(data)} members in {guildName}{Style.RESET_ALL}")


def getVersion():
    version = "1.10.7"
    return version

def buildContextProperites(channelId, guildId) -> str:
    """Builds the context properties header which we need to use while joining the guild. It is not required but sending this as well will decrease the chance of your token getting locked so yeah."""
    return b(dumps({"location":"Join Guild","location_guild_id":guildId,"location_channel_id":channelId,"location_channel_type":0}, separators=(',', ':')).encode()).decode()
if __name__ == "__main__":
    print(buildContextProperites("906184472716783626", "906181942247055400"))
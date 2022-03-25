# Made by Shahzain
# Libs
import httpx
import pyfiglet
import sys
import threading
import time
import json
import random
import os
# ===================================================== #
from colorama import Fore, Style
from massdm import MassDM
from multiprocessing.pool import ThreadPool as Pool
from globalvariables import sockStatus, qurantinedTokens, sentUsers, blacklistedUsers, unqurantineToken
from utils import scrapeMembers, showMenu, scrapeMassMention, getInviteInfo, getGoodToken, buildContextProperites
from update import lookforupdates

def clearConsole(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


clearConsole()
print(Fore.BLUE + Style.BRIGHT + """
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ███╗   ███╗██╗   ██╗██╗     ████████╗██╗████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ████╗ ████║██║   ██║██║     ╚══██╔══╝██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██╔████╔██║██║   ██║██║        ██║   ██║   ██║   ██║   ██║██║   ██║██║     
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║╚██╔╝██║██║   ██║██║        ██║   ██║   ██║   ██║   ██║██║   ██║██║     
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██║ ╚═╝ ██║╚██████╔╝███████╗   ██║   ██║   ██║   ╚██████╔╝╚██████╔╝███████╗
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                                                                                                                        P Y T H O N
""" + Style.RESET_ALL)
print(f'{Style.BRIGHT}By Shahzain\n\n')
lookforupdates()
with open("input/tokens.txt") as fp:
    tokens = fp.read().splitlines()
with open("config.json") as fp:
    config = json.load(fp)
if os.path.exists("hcap.py") == False:
    print(f"{Fore.YELLOW}{Style.BRIGHT}[?] Hcaptcha solver file was not found. Downloading it..{Style.RESET_ALL}")
    f = httpx.get("https://raw.githubusercontent.com/shahzain345/Discord-MultiToolPY/main/hcap.py").text
    open("hcap.py", "w", encoding="utf-8").write(f)
    print(f"[{Fore.LIGHTCYAN_EX}{Style.BRIGHT}SUCCESS{Style.RESET_ALL}] {Fore.GREEN}{Style.BRIGHT}Hcaptcha solver file downloaded. \nPlease restart the tool {Style.RESET_ALL}")
    exit()
if os.path.exists("input/usernames.txt") == False:
    print(f"{Fore.YELLOW}{Style.BRIGHT}[?] Usernames file was not found. Making it..{Style.RESET_ALL}")
    open("input/usernames.txt", "w").write("shahzain345")
    print(f"[{Fore.LIGHTCYAN_EX}{Style.BRIGHT}SUCCESS{Style.RESET_ALL}] {Fore.GREEN}{Style.BRIGHT}Usernames file created. \nPlease restart the tool {Style.RESET_ALL}")
    exit()
if len(tokens) == 0:
    print(
        f"{Fore.RED}{Style.BRIGHT}[?] Input some tokens before restarting! {Style.RESET_ALL}")
    input(f"{Style.BRIGHT}Press enter to exit {Style.RESET_ALL}")
    quit()
if len(open("input/proxies.txt").read().splitlines()) == 0 and config["proxyless"] == False:
    print(
        f"{Fore.RED}{Style.BRIGHT}[?] Input some proxies before restarting! {Style.RESET_ALL}")
    input(f"{Style.BRIGHT}Press enter to exit {Style.RESET_ALL}")
    quit()
def setTitle(tokens: list): return os.system(
    f'title Discord MassDM - Tokens: {len(tokens)} - Proxies: {len(open("input/proxies.txt").read().splitlines())} - By Shahazain' if os.name == "nt" else f'echo -n -e "\033]0;Discord MassDM | Tokens {len(tokens)} | Proxies {len(open("input/proxies.txt").read().splitlines())} - By Shahzain\007"'
)


goodtokens = []


def checkToken(token):
    massDm = MassDM(token)
    o = massDm.checkToken()
    if o != "Invalid":
        goodtokens.append(token)


def joinServer(token, rawInvite, delay, messageId, channelId, ctx):
    time.sleep(delay)
    massDm = MassDM(token)
    o, resJSON = massDm.joinServer(rawInvite, ctx)
    if o != "Joined":
        return None
    else:
        guildId = resJSON["guild"]["id"]
        if resJSON["show_verification_form"] == True and config["bypass_membership_screening"] == True:
            massDm.memberShipScreening(guildId, rawInvite)
        if messageId != None:
            emojiObject = massDm.getReactions(messageId, channelId)
            massDm.createReaction(messageId, channelId, emojiObject)
        return True

def onlineToken(token):
    massDm = MassDM(token)
    massDm.websocketToken()


def changeFormat(token: str):
    if ":" not in token or len(token.split(":")) == 2:
        token = token if ":" not in token else token.split(":")[1]
        print(
            f"{Fore.RED}{Style.BRIGHT}{token} format is not [Email:Pass:Token]{Style.RESET_ALL}")
        return token
    newToken = token.split(":")[2]
    print(f"{Fore.GREEN}{Style.BRIGHT}{token} => {newToken}")
    return newToken


def serverLeaver(token: str, guildId):
    u = MassDM(token)
    u.leaveServer(guildId)


def sendDM(token, message, user, delay=None):
    if delay is not None:
        time.sleep(int(delay))
        massDm = MassDM(token)
        d = massDm.sendDM(message, user)
        if 'You are opening direct messages too fast' in d.text:
            qurantinedTokens.append(token)
            threading.Thread(target=unqurantineToken, args=(token, )).start()
            print(
                f"{Fore.GREEN}{Style.BRIGHT}{token} is ratelimited{Style.RESET_ALL}")
        elif 'Cannot send messages to this user' in d.text:
            blacklistedUsers.append(user)
        elif 'You need to verify your account in order to perform this action' in d.text or '401: Unauthorized' in d.text:
            qurantinedTokens.append(token)
            print(
                f"{Fore.RED}{Style.BRIGHT}{token} got locked during testing{Style.RESET_ALL}")
    else:
        massDm = MassDM(token)
        d = massDm.sendDM(message, user)
        if 'You are opening direct messages too fast' in d.text:
            qurantinedTokens.append(token)
            threading.Thread(target=unqurantineToken, args=(token, )).start()
            print(
                f"{Fore.GREEN}{Style.BRIGHT}{token} is ratelimited{Style.RESET_ALL}")
        elif 'Cannot send messages to this user' in d.text:
            blacklistedUsers.append(user)
        elif 'You need to verify your account in order to perform this action' in d.text or '401: Unauthorized' in d.text:
            qurantinedTokens.append(token)
            print(
                f"{Fore.RED}{Style.BRIGHT}{token} got locked during testing{Style.RESET_ALL}")
def reactionAdder(token, messageId, channelId):
    l = MassDM(token)
    emojiObject = l.getReactions(messageId, channelId)
    l.createReaction(messageId, channelId, emojiObject)
    print(f"{Fore.GREEN}{Style.BRIGHT}Added reaction on: {messageId}{Style.RESET_ALL}")
def spamDm(token, userId, message):
    massdn = MassDM(token=token)
    while True:
        massdn.sendDM(message, userId)


def bioChanger(token, newbio):
    o = MassDM(token)
    o.changeBio(newbio)


def spamServer(token, channelId, message, massMention, massMentionSize):
    massDm = MassDM(token)
    while True:
        massDm.sendMessageInChannel(
            channelId, message, massMention, massMentionSize)
def changeUsername(token: str):
    if ":" not in token:
        print(f"{Fore.RED}{Style.BRIGHT}{token} is not [Email:Pass:Token]{Style.RESET_ALL}")
        return None
    t = token.split(":")[2]
    p = token.split(":")[1].split(":")[0]
    md = MassDM(t)
    md.changeUsername(random.choice(open("input/usernames.txt").read().splitlines()), p)

def serverCheck(token, guildId):
    massDm = MassDM(token)
    res = massDm.getGuild(guildId)
    if "name" not in res:
        print(
            f"{Fore.RED}{Style.BRIGHT}{token} is not in server: {guildId}{Style.RESET_ALL}")
        return False
    else:
        print(
            f"{Fore.GREEN}{Style.BRIGHT}{token} is in server: {res['name']}{Style.RESET_ALL}")
        return True


def menu():
  try:
    tokens = open("input/tokens.txt").read().splitlines()
    config = json.load(open("config.json"))
    setTitle(tokens)
    showMenu()
    choice = int(input(
        f"\n\n{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Enter your choice: \n>> {Style.RESET_ALL}"))
    choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    if choice not in choices:
        print(f"{Fore.RED}{Style.BRIGHT}Invalid Choice{Style.RESET_ALL}\n")
        return menu()
    if choice == 1:
        print(f"{Fore.GREEN}Checking Tokens {Style.RESET_ALL}")
        pool_Count = int(input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter thread count (Enter 0 for prefered settings): {Style.RESET_ALL}"))
        pool_size = 1000 if pool_Count == 0 else pool_Count
        pool = Pool(pool_size)
        for token in tokens:
            pool.apply_async(checkToken, (token, ))
        pool.close()
        pool.join()
        if config["removeDeadTokens"] == True:
            open('input/tokens.txt', 'w').write("")
            with open("input/tokens.txt", "a") as fp:
                for token in goodtokens:
                    fp.write(token + "\n")
        goodtokens.clear()
        return menu()
    if choice == 2:
        rawInvite = str(input(f"{Fore.GREEN}{Style.BRIGHT}Enter your invite: {Style.RESET_ALL}")).split(
            "discord.gg/")[1]
        messageId = None if config["bypass_reaction_verification"] == False else str(input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter the messageId the reaction is on: {Style.RESET_ALL}"))
        channelId = None if config["bypass_reaction_verification"] == False else str(input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter the channelId the message is on: {Style.RESET_ALL}"))
        req1 = getInviteInfo(rawInvite)
        if req1 == {"message": "Unknown Invite", "code": 10006}:
            print(
                f"{Fore.RED}{Style.BRIGHT}Invalid Invite: {rawInvite}{Style.RESET_ALL}")
            return menu()
        else:
            print(
                f"{Fore.GREEN}{Style.BRIGHT}Valid Invite: {rawInvite}{Style.RESET_ALL}")
        delay = int(input(f"{Fore.GREEN}{Style.BRIGHT}Enter delay (seconds): {Style.RESET_ALL}")
                    ) if config["useDelays"] == True else 0
        ctxproperties = buildContextProperites(req1["channel"]["id"], req1["guild"]["id"])
        pool = Pool(1000)
        for token in tokens:
            pool.apply_async(joinServer, (token, rawInvite, delay, messageId, channelId, ctxproperties)) if config["useDelays"] == False else pool.apply(
                joinServer, (token, rawInvite, delay, messageId, channelId, ctxproperties))
        pool.close()
        pool.join()
        return menu()
    if choice == 3:
        pool = Pool(20)
        for token in tokens:
            pool.apply_async(onlineToken, (token, ))
        input("Press Enter to close the websocket?(All tokens will go offline)")
        sockStatus = "Close"
        pool.close()
        pool.join()
        return menu()
    if choice == 4:
        print(
            f"{Fore.GREEN}{Style.BRIGHT}Changing format to [token]..{Style.RESET_ALL}")
        newTokens = []
        for token in tokens:
            newToken = changeFormat(token)
            newTokens.append(newToken)
        open("input/tokens.txt", "w").write("")
        with open("input/tokens.txt", "a") as fp:
            for token in newTokens:
                fp.write(token + "\n")
        return menu()
    if choice == 5:
        print(f"{Fore.GREEN}{Style.BRIGHT}Starting Mass DM{Style.RESET_ALL}")
        channelId = str(
            input(f"{Fore.GREEN}{Style.BRIGHT}Enter channelId to scrape:{Style.RESET_ALL}"))
        o = MassDM(getGoodToken())
        guild = o.getChannel(channelId)
        scrapeMembers(getGoodToken(), guild, channelId)
        scrappedMembers = open("scraped/members.txt").read().splitlines()
        filteredMembers = list(
            filter(lambda member: member not in sentUsers, scrappedMembers))
        pool = Pool(450)
        messageObj = json.load(open("message.json"))
        delay = input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter delay (seconds): {Style.RESET_ALL}") if config["useDelays"] == True else None
        for userId in filteredMembers:
            if userId in sentUsers or userId in blacklistedUsers:
                continue
            if config["sendMultitpleMessages"] == True:
                good_token = getGoodToken()
                for msg in messageObj:
                    variableReplacedMsg = str(msg["content"]).replace(
                        "<@user>", f"<@{userId}>")
                    pool.apply_async(sendDM, (good_token, variableReplacedMsg, userId, delay)) if config["useDelays"] == False else pool.apply(
                        sendDM, (getGoodToken(), variableReplacedMsg, userId, delay))
            variableReplacedMsg = str(messageObj[0]["content"]).replace(
                        "<@user>", f"<@{userId}>")
            pool.apply_async(sendDM, (getGoodToken(), variableReplacedMsg, userId, delay)) if config["useDelays"] == False else pool.apply(
                sendDM, (getGoodToken(), variableReplacedMsg, userId, delay))
        return menu()
    if choice == 12:
        print(f"{Fore.GREEN}{Style.BRIGHT}Spamming server{Style.RESET_ALL}")
        massMention = True if input(
            f"{Fore.GREEN}{Style.BRIGHT}Do you want to use massmention? (y/n){Style.RESET_ALL}").lower() == "y" else None
        massMentionSize = None if massMention != True else int(input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter the ammount of people you want to mention in one message: {Style.RESET_ALL}"))
        message = input(
            f"{Fore.GREEN}{Style.BRIGHT}Please type the message: {Style.RESET_ALL}")
        channelId = input(
            f"{Fore.GREEN}{Style.BRIGHT}Please enter the channelId you want to spam: {Style.RESET_ALL}")
        pool_Count = int(input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter thread count (Enter 0 for prefered settings): {Style.RESET_ALL}"))
        o = MassDM(token=random.choice(tokens))
        guild = str(o.getChannel(channelId))
        if massMention == True:
            scrapeMassMention(random.choice(tokens), guild, channelId)
        pool_size = 1000 if pool_Count == 0 else pool_Count
        pool = Pool(pool_size)
        for token in tokens:
            pool.apply_async(spamServer, (token, channelId,
                             message, massMention, massMentionSize))
        pool.close()
        pool.join()
        return menu()
    if choice == 6:
        print(f"{Fore.GREEN}{Style.BRIGHT}Spamming DMS{Style.RESET_ALL}")
        message = input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter the message: {Style.RESET_ALL}")
        userId = input(
            f"{Fore.GREEN}{Style.BRIGHT}Enter the userId: {Style.RESET_ALL}")
        pool = Pool(1000)
        for token in tokens:
            pool.apply_async(spamDm, (token, userId, message))
        pool.close()
        pool.join()
        return menu()
    if choice == 7:
        print(f"{Fore.GREEN}{Style.BRIGHT}Changing usernames..{Style.RESET_ALL}")
        pool = Pool(1000)
        for token in tokens:
            pool.apply_async(changeUsername, (token, ))
        pool.close()
        pool.join()
        return menu()
    if choice == 8:
        print(f"{Fore.GREEN}{Style.BRIGHT}Member scrapper{Style.RESET_ALL}")
        cId = input(
            f"{Fore.GREEN}{Style.RESET_ALL}Enter the channelId: {Style.RESET_ALL}")
        gId = MassDM(random.choice(tokens)).getChannel(cId)
        scrapeMembers(getGoodToken(), gId, cId)
    if choice == 13:
        os.system("cls") if os.name in ("nt", "dos") else os.system("clear")
        print(Fore.GREEN + pyfiglet.figlet_format("Credits"))
        print(f"{Fore.GREEN}{Style.BRIGHT}This tool was created by Shahzain345: github.com/shahzain345{Style.RESET_ALL}\n")
        print(f"{Fore.BLUE}{Style.BRIGHT}If someone sold you this tool you got scammed, dm me on discord if that happens!{Style.RESET_ALL}\n")
        input(
            f"{Fore.CYAN}{Style.BRIGHT}Press enter to return to menu: {Style.RESET_ALL}")
        return menu()

    if choice == 11:
        print(f"{Fore.GREEN}{Style.BRIGHT}Server checker{Style.RESET_ALL}")
        guildId = str(
            input(f"{Fore.GREEN}{Style.BRIGHT}Please enter the serverId: {Style.RESET_ALL}"))
        pool = Pool(1000)
        for token in tokens:
            pool.apply_async(serverCheck, (token, guildId))
        pool.close()
        pool.join()
        return menu()
    if choice == 14:
        print(f'{Fore.GREEN}{Style.BRIGHT}Bio changer{Style.RESET_ALL}')
        bios = open("input/bios.txt").read().splitlines()
        pool = Pool(1000)
        for token in tokens:
            pool.apply_async(bioChanger, (token, random.choice(bios)))
        pool.close()
        pool.join()
        return menu()
    if choice == 15:
        print(f"{Fore.GREEN}{Style.BRIGHT}Reaction spammer{Style.RESET_ALL}")
        messageId = input(f"{Fore.GREEN}{Style.BRIGHT}Enter the messageId of the message the reaction is on: {Style.RESET_ALL}")
        channelId = input(f"{Fore.GREEN}{Style.BRIGHT}Enter the channelId of the channel the message is on: {Style.RESET_ALL}")
        pool = Pool(2000)
        for token in tokens:
            pool.apply_async(reactionAdder, (token, messageId, channelId))
        pool.close()
        pool.join()
        return menu()
    if choice == 17:
        choice2 = input(
            f"{Fore.RED}{Style.BRIGHT}Are you sure you want to exit?: (y/n){Style.RESET_ALL}").lower()
        if choice2 != "y":
            return menu()
        clearConsole()
        intNum = 3
        for i in range(4):
            print(Fore.GREEN +
                  pyfiglet.figlet_format(f"Exiting in: {intNum-i}s"))
            time.sleep(1)
            clearConsole()
        print(Fore.GREEN + Style.BRIGHT +
              pyfiglet.figlet_format("Thank You For Using This Tool") + Style.RESET_ALL)
        print(f"{Style.BRIGHT}By Shahzain{Style.RESET_ALL}")
        quit()
    if choice == 10:
        print(f"{Fore.GREEN}{Style.BRIGHT}Server leaver{Style.RESET_ALL}")
        guildId = str(
            input(f"{Fore.GREEN}Enter the server Id: {Style.RESET_ALL}"))
        pool = Pool(1000)
        for token in tokens:
            pool.apply_async(serverLeaver, (token, guildId, ))
        pool.close()
        pool.join()
        return menu()
    if choice == 16:
        clearConsole()
        print(f"{Fore.GREEN}{Style.BRIGHT}Showing configuration{Style.RESET_ALL}")
        for configuration in config.items():
            print(f'[{Fore.GREEN}>{Style.RESET_ALL}] {configuration[0]}: {configuration[1]} \n')
        input("Press enter to return back to menu")
        return menu()
    if choice == 18:
        os.execv(sys.executable, ['python'] + sys.argv)
        exit()
  except Exception as e:
       print(f"{Fore.RED}{Style.BRIGHT}[?] Exception: {e} {Style.RESET_ALL}")
       return menu()
print(f"{Style.RESET_ALL}[{Fore.LIGHTRED_EX}{Style.BRIGHT}WARNING{Style.RESET_ALL}]{Fore.YELLOW}{Style.BRIGHT} Proxyless is on!, please switch to proxies if you want to avoid ratelimits{Style.RESET_ALL}") if config["proxyless"] == True else None
print(f"{Style.RESET_ALL}[{Fore.LIGHTRED_EX}{Style.BRIGHT}WARNING{Style.RESET_ALL}]{Fore.YELLOW}{Style.BRIGHT} Hcaptcha solver is currently disabled due to some issues. {Style.RESET_ALL}\n\n")
menu()

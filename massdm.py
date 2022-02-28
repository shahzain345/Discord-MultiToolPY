import httpx
import time
from colorama import Fore, Style
from globalvariables import getQurantinedToken, qurantineToken, sentUsers, sockStatus
from urllib.parse import urlencode
import random
import string
import json as theJson
import websocket
# Main MassDm class

config = theJson.load(open("config.json"))
def savelogs(logType, message):
    if config["save_failed_logs"] == False:
        return None
    if logType == "invite":
        open("logs/invitelogs.txt", 'a').write(message + "\n")
    elif logType == "dm":
        open("logs/dmlogs.txt", 'a').write(message + "\n")
    elif logType == "spam":
        open("logs/spammerlogs.txt", 'a').write(message + "\n")
    return True


class MassDM:
    def __init__(self, token):
        proxies = open("input/proxies.txt").read().splitlines()
        self.client = httpx.Client(cookies={"locale": "en-US"}, headers={"Pragma": "no-cache", "Accept": "*/*", "Host": "discord.com", "Accept-Language": "en-US", "Cache-Control": "no-cache", "Accept-Encoding": "br, gzip, deflate", "Referer": "https://discord.com/", "Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
                                                                         "X-Track": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi11cyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzEzXzYpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xMy4xLjIgU2FmYXJpLzYwNS4xLjE1IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMuMS4yIiwib3NfdmVyc2lvbiI6IjEwLjEzLjYiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTEzNTQ5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="}, proxies=f"{config['proxyProtocol']}://{random.choice(proxies)}") if config["proxyless"] == False else httpx.Client(cookies={"locale": "en-US"}, headers={"Pragma": "no-cache", "Accept": "*/*", "Host": "discord.com", "Accept-Language": "en-US", "Cache-Control": "no-cache", "Accept-Encoding": "br, gzip, deflate", "Referer": "https://discord.com/", "Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
                                                                         "X-Track": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi11cyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzEzXzYpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xMy4xLjIgU2FmYXJpLzYwNS4xLjE1IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMuMS4yIiwib3NfdmVyc2lvbiI6IjEwLjEzLjYiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTEzNTQ5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="})
        superproperties = self.client.headers["X-Track"]
        self.client.headers["X-Fingerprint"] = self.client.get(
            "https://discord.com/api/v9/experiments", timeout=30).json()["fingerprint"]
        del self.client.headers["X-Track"]
        self.client.headers["X-Super-Properties"] = superproperties
        self.client.headers["Authorization"] = token
        self.client.headers["Origin"] = "https://discord.com"
        self.config = theJson.load(open("config.json"))

    def createChat(self, userId):
        """Creates a DM channel with userId and returns channelId or None"""
        req = self.client.post(
            "https://discord.com/api/v9/users/@me/channels", json={"recipients": [userId]})
        if req.status_code != 200:
            return None
        else:
            return req.json()['id']

    def getRandomNonce(self):
        """Returns a random str with numbers only, len=18, this is required for sending messages"""
        return "".join(random.choice(string.digits) for i in range(18))

    def getCap(self):
        captchaApi = self.config["captcha_api"]
        captchaKey = self.config["captcha_key"]
        solvedCaptcha = None
        taskId = ""
        taskId = httpx.post(f"https://api.{captchaApi}/createTask", json={"clientKey": captchaKey, "task": {"type": "HCaptchaTaskProxyless", "websiteURL": "https://discord.com/",
                            "websiteKey": "4c672d35-0701-42b2-88c3-78380b0db560", "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}}, timeout=30).json()
        if taskId.get("errorId") > 0:
            print(f"[-] createTask - {taskId.get('errorDescription')}!")
            return None
        taskId = taskId.get("taskId")

        while not solvedCaptcha:
            captchaData = httpx.post(f"https://api.{captchaApi}/getTaskResult", json={
                                     "clientKey": captchaKey, "taskId": taskId}, timeout=30).json()
            if captchaData.get("status") == "ready":
                solvedCaptcha = captchaData.get(
                    "solution").get("gRecaptchaResponse")
                return solvedCaptcha
    def sendFriendRequest(self, username, discrim) -> httpx.Response:
        """Sends a friend request to the given user returns httpx.Response, will add this soon cuz i am tired 😃"""
        return None
    def sendDM(self, message, userId) -> httpx.Response:
        """Sends a dm to the given userId"""
        try:
            channelId = self.createChat(userId)
            req = self.client.post(f'https://discord.com/api/v9/channels/{channelId}/messages', json={
                "content": message,
                "tts": False,
                "nonce": self.getRandomNonce()
            })
            if req.status_code != 200:
                print(
                    f'{Style.BRIGHT}{Fore.RED}[>] Failed to send message to {userId}{Style.RESET_ALL}')
                savelogs(
                    "dms", f"{self.client.headers['Authorization']} failed to send dm to {userId}")
                return req
            else:
                print(
                    f'{Style.BRIGHT}{Fore.GREEN}[>] Sent message, messageId: {req.json()["id"]}{Style.RESET_ALL}')
                sentUsers.append(userId)
                return req
        except:
            print(
                f"{Fore.RED}{Style.BRIGHT}A httpx exception was raised{Style.RESET_ALL}")

    def checkToken(self):
        """Checks the token to see if its valid or invalid returns a str "Valid" | "Invalid" """
        req = self.client.get(
            "https://discord.com/api/v9/users/@me/affinities/guilds")
        if req.status_code == 400 or req.status_code > 400:
            print(
                f"{Fore.RED}{Style.BRIGHT}{self.client.headers['Authorization']} is invalid {Style.RESET_ALL}")
            return "Invalid"
        else:
            print(
                f"{Fore.GREEN}{Style.BRIGHT}{self.client.headers['Authorization']} is valid {Style.RESET_ALL}")
            return "Valid"

    def joinServer(self, rawInvite):
        """Joins self.token to rawInvite, returns a str "Joined" | "NotJoined" """
        req = self.client.post(
            f"https://discord.com/api/v9/invites/{rawInvite}", json={"captcha_key": self.getCap()})
        if req.status_code == 200:
            print(
                f"{Fore.GREEN}{self.client.headers['Authorization']} joined server! {Style.RESET_ALL}")
            return "Joined", req.json()
        else:
            print(
                f"{Fore.RED}{self.client.headers['Authorization']} failed to join server! {Style.RESET_ALL}")
            savelogs(
                "invite", f"{self.client.headers['Authorization']} failed to join {rawInvite}")
            return "NotJoined", req.json()

    def changeUsername(self, newUsername, password):
        """Changes the username of self.token, returns nothing"""
        req = self.client.patch("https://discord.com/api/v9/users/@me", json={
            "password": password,
            "username": newUsername
        })
        if req.status_code == 200:
            print(
                f"{Fore.GREEN}{self.client.headers['Authorization']} Username changed to {newUsername} {Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}{self.client.headers['Authorization']} Failed to change username to {newUsername}")

    def websocketToken(self):
        """Opens a websocket with discord"""
        sock_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?encoding=json&v=9",
                   header=sock_headers)
        ws.send('{"op":2,"d":{"token":"' + self.client.headers["Authorization"] + '","capabilities":125,"properties":{"os":"Windows","browser":"Firefox","device":"","system_locale":"it-IT","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0","browser_version":"94.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}')
        print(
            f"{Fore.GREEN}{Style.BRIGHT}Websocket opened {self.client.headers['Authorization']}{Style.RESET_ALL}")
        while sockStatus == "Open":  # heartbeating
            ws.send('{"op":1,"d":' + str(0) + '}')
            time.sleep(5)
        ws.close()

    def sendMessageInChannel(self, channelId, message, massMention=None, massMentionSize=None):
        """Returns a JSON object which has the message properties, read more in github.com/shahzain345"""
        payload = {
            "content": None,
            "tts": False,
            "nonce": self.getRandomNonce()
        }
        if massMention is not None:
            scrappedMembers = open(
                "scraped/massmention.txt").read().splitlines()
            mentions = "".join(
                f'<@{random.choice(scrappedMembers)}> ' for i in range(massMentionSize))
            # <@{random.choice(scrappedMembers)}> <@{random.choice(scrappedMembers)}>
            payload["content"] = f'{mentions} \n {message}'
        else:
            payload["content"] = message
        req = self.client.post(
            f'https://discord.com/api/v9/channels/{channelId}/messages', json=payload)
        if req.status_code != 200:
            print(
                f'{Style.BRIGHT}{Fore.RED}[>] Failed to send message in {channelId}{Style.RESET_ALL}')
            savelogs(
                "spam", f"{self.client.headers['Authorization']} failed to send message in {channelId}")
            return req.json()
        else:
            print(
                f'{Style.BRIGHT}{Fore.GREEN}[>] Sent message, messageId: {req.json()["id"]}{Style.RESET_ALL}')
            return req.json()

    def getChannel(self, channelId):
        """Returns id of the server the channel is in"""
        req = self.client.get(
            f"https://discord.com/api/v9/channels/{channelId}")
        if 'guild_id' not in req.json():
            print(f"{Fore.RED}{Style.BRIGHT}Guild Id not found{Style.RESET_ALL}")
            guildId = input(
                f"{Fore.GREEN}{Style.BRIGHT}Please enter the guild Id{Style.RESET_ALL}")
            return guildId
        guildId = req.json()["guild_id"]
        if not guildId:
            return None
        return guildId

    def getGuild(self, guildId):
        """Returns guild object: https://discord.com/developers/docs/resources/guild#guild-object"""
        req = self.client.get(f"https://discord.com/api/v9//guilds/{guildId}")
        if "name" not in req.json():
            print(
                f"{Fore.RED}{Style.BRIGHT}Invalid JSON returned from discord{Style.RESET_ALL}")
            print(req.json())
            return req.json()
        return req.json()

    def changeBio(self, newBio):
        """Changes bio of self.token to newBio"""
        req = self.client.patch("https://discord.com/api/v9/users/@me", json={
            "bio": newBio
        })
        if req.status_code != 200:
            print(
                f"{Fore.RED}{Style.BRIGHT}{self.client.headers['Authorization']} failed to change bio to {newBio}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.GREEN}{Style.BRIGHT}{self.client.headers['Authorization']} changed bio to {newBio}{Style.RESET_ALL}")

    def leaveServer(self, guildId):
        req = self.client.delete(
            f"https://discord.com/api/v9/users/@me/guilds/{guildId}")
        if req.status_code != 204:
            print(
                f'{Fore.RED}{Style.BRIGHT}[>] Failed to leave guild{Style.RESET_ALL}')
        else:
            print(
                f'{Fore.GREEN}{Style.BRIGHT}[>] Left guild {guildId}{Style.RESET_ALL}')

    def memberShipScreening(self, guildId, rawInvite):
        """Bypasses membership screening 😃"""
        # First request 1, gets json
        req = self.client.get(
            f"https://discord.com/api/v9/guilds/{guildId}/member-verification?with_guild=false&invite_code={rawInvite}")
        if req.status_code != 200:
            print(
                f"{Fore.RED}{Style.BRIGHT}Failedt to bypass membership screening for {guildId}{Style.RESET_ALL}")
        req = self.client.put(
            f"https://discord.com/api/v9/guilds/{guildId}/requests/@me", json=req.json())

    def getMessage(self, messageId, channelId):
        """Gets the message, returns a message object 😃"""
        req = self.client.get(
            f"https://discord.com/api/v9/channels/{channelId}/messages?limit=1&around={messageId}")
        return req.json() 

    def getReactions(self, messageId, chanenlId):
        try:
            mesasgeObject = self.getMessage(messageId, chanenlId)
            mesasgeObject = mesasgeObject[0]
            reactions = list(mesasgeObject["reactions"])
            firstEmoji = reactions[0]["emoji"]
            return firstEmoji
        except Exception as e:
            print(e)
            return None

    def createReaction(self, messageId, channelId, emojiObject):
        try:
            req = self.client.put(
                f"https://discord.com/api/v9/channels/{channelId}/messages/{messageId}/reactions/{emojiObject['name']}%3A{emojiObject['id']}/%40me")
            if req.status_code != 204:
                print(
                    f"{Fore.RED}{Style.BRIGHT}Failed to bypass reaction verification{Style.RESET_ALL}")
                return req.json()
            else:
                return req.json()
        except Exception as e:
            print(e)
            return None
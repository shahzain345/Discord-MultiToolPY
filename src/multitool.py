"""
Copyright 2022 Shahzain Masood

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from httpx import AsyncClient
from ._utility import Utility, MPrint
from ._captcha import Captcha
from base64 import b64encode as encoder
from colorama import Fore, Style
from .discordsocket import DiscordSocket
import websocket
import random
import time
import json as jsonLib
import string
console = MPrint()
BUILD_NUM = Utility().getBuildNum()
console.s_print(f"Discord is currently on build: {BUILD_NUM}")
time.sleep(1.5)

class MultiTool:
    """
    # Multitool main class
    """
    async def _init(self, token: str):
        self._utility = Utility()
        self.client = AsyncClient(proxies=self._utility.proxy, cookies={"locale": "en-US"}, headers={
            "Accept": "*/*",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Language": "en-us",
            "Host": "discord.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
            "Referer": "https://discord.com/",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive"
        }, timeout=self._utility.config["requestTimeout"])
        self.token = token
        self.client.headers["X-Track"] = self._build_trackers(
            trackerType="x-track")
        res = await self.client.get(
            "https://discord.com/api/v9/experiments")
        try:
            self.client.headers["X-Fingerprint"] = res.json().get("fingerprint")
        except:
            #self.client.headers["X-Fingerprint"] = "992405718051344425.40u0H3W3P2iOxVPP-50_HbyxbcI"
            None # do nothing if fingerprint aint found, cuz fingerprint isn't needed anyways just improves your success rate
        self.client.headers["Origin"] = "https://discord.com/"
        self.client.headers["Authorization"] = token
        self.client.headers["X-Debug-Options"] = "bugReporterEnabled"
        self.client.headers["X-Discord-Locale"] = "en-US"
        self.client.headers["Referer"] = "https://discord.com/channels/@me"
        del self.client.headers["X-Track"]
        self.client.headers["X-Super-Properties"] = self._build_trackers(
            trackerType="x-super-properties")
        self._captcha = Captcha()

    def _build_trackers(self, trackerType: str) -> str:
        """Builds the x-track/x-super-properties header"""
        if trackerType == "x-track":
            return encoder(jsonLib.dumps({"os": "Mac OS X", "browser": "Safari", "device": "", "system_locale": "en-us", "browser_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15", "browser_version": "13.1.2", "os_version": "10.13.6", "referrer": "", "referring_domain": "", "referrer_current": "", "referring_domain_current": "", "release_channel": "stable", "client_build_number": 9999, "client_event_source": None}, separators=(',', ':')).encode()).decode()
        elif trackerType == "x-super-properties":
            return encoder(jsonLib.dumps({"os": "Mac OS X", "browser": "Safari", "device": "", "system_locale": "en-us", "browser_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15", "browser_version": "13.1.2", "os_version": "10.13.6", "referrer": "", "referring_domain": "", "referrer_current": "", "referring_domain_current": "", "release_channel": "stable", "client_build_number": BUILD_NUM, "client_event_source": None}, separators=(',', ':')).encode()).decode()
        else:
            raise Exception(
                "Invalid tracker type. Currently support types('x-track', 'x-super-properties')")

    async def join(self, rawInvite: str, ctxProperties: str):
        self.client.headers["X-Context-Properties"] = ctxProperties
        req = await self.client.post(
            f"https://discord.com/api/v9/invites/{rawInvite}", json={})
        if "captcha_key" not in req.json():
            if req.json().get("message") == "The user is banned from this guild.":
                console.f_print(f"{self.token} is banned from this server.")
                return False, req
            console.s_print(
                f"{self.token} successfully joined discord.gg/{rawInvite}")
            return True, req
        console.w_print(f"{self.token} captcha detected. solving thru {self._utility.config.get('captcha').get('api')}")
        captcha_sitekey = req.json()["captcha_sitekey"]
        captcha_rqtoken = req.json()["captcha_rqtoken"]
        captcha_rqdata = req.json()["captcha_rqdata"]
        captcha_key = await self._captcha.getCaptcha(captcha_sitekey, captcha_rqdata)
        req = await self.client.post(f"https://discord.com/api/v9/invites/{rawInvite}", json={
            "captcha_key": captcha_key,
            "captcha_rqtoken": captcha_rqtoken
        })
        if req.status_code == 200:
            console.s_print(
                f"{self.token} successfully joined discord.gg/{rawInvite}")
            return True, req
        else:
            console.f_print(
                f"{self.token} failed to join discord.gg/{rawInvite}")
            return False, req

    async def bypassScreening(self, guildId: str, rawInvite: str):
        req = await self.client.get(
            f"https://discord.com/api/v9/guilds/{guildId}/member-verification?with_guild=false&invite_code={rawInvite}")
        if req.status_code != 200:
            console.f_print(
                f"{self.token} failed to bypass membership screening!")
            return False
        req = await self.client.put(
            f"https://discord.com/api/v9/guilds/{guildId}/requests/@me", json=req.json())
        console.s_print(
            f"{self.token} bypassed membership screening for {guildId}(discord.gg/{rawInvite}) successfully!")
        return True

    def __random_nonce(self):
        """Returns a random str with numbers only, len=18, this is required for sending messages"""
        return "".join(random.choice(string.digits) for _ in range(18))

    async def __send_message(self, payload: dict, channelId: str):
        return await self.client.post(f'https://discord.com/api/v9/channels/{channelId}/messages', json=payload)

    async def __open_dm(self, userId: str):
        req = await self.client.post(
            "https://discord.com/api/v9/users/@me/channels", json={"recipients": [userId]})
        if req.status_code != 200:
            console.f_print(f"{self.token} failed to open dm with {userId}")
            return None, req
        else:
            return req.json()['id'], req

    async def sendDirectMessage(self, userId: str, message: str):
        """Sends a direct message to <@userId>"""
        channelId, req = await self.__open_dm(userId)
        if channelId == None:
            return None, req  # do nothing if it failed to open dms with <@userId>
        payload = {
            "content": message,
            "tts": False,
            "nonce": self.__random_nonce()
        }
        res = await self.__send_message(payload, channelId)
        if res.status_code == 200:
            return True, res
        else:
            return False, res

    async def sendMessageInChannel(self, message: str, channelId: str, massMention: bool = False, massMentionSize: int = 6):
        scrappedMembers = open("scraped/massmention.txt").read().splitlines()
        if len(scrappedMembers) < 1 and massMention:
            console.f_print(
                f"{self.token} server has 0 members. thus mass mention wont work")
            return False
        payload = {
            "content": None,
            "tts": False,
            "nonce": self.__random_nonce()
        }
        if massMention:
            mentions = "".join(
                f'<@{random.choice(scrappedMembers)}> ' for _ in range(massMentionSize))
            payload["content"] = f"{mentions}\n{message}"
        else:
            payload["content"] = message
        req = await self.__send_message(payload, channelId)
        if req.status_code == 200:
            console.s_print(
                f"{self.token} successfully sent message in {channelId}")
            return True
        else:
            console.f_print(
                f"{self.token} failed to send message in {channelId}")
            return False

    async def checkToken(self):
        req = await self.client.get(
            "https://discord.com/api/v9/users/@me/affinities/guilds")
        if req.status_code == 403:
            console.f_print(f"{self.token} is [LOCKED]")
            return False, "LOCKED"
        elif req.status_code == 401:
            console.f_print(f"{self.token} is {Fore.RESET}{Fore.YELLOW}[INVALID]{Fore.RESET}")
            return False, "INVALID"
        else:
            console.s_print(f"{self.token} is [VALID]")
            return True, "VALID"

    async def getGuild(self, guildId: str):
        req = await self.client.get(f"https://discord.com/api/v9//guilds/{guildId}")
        if "name" not in req.json():
            console.f_print(f"{self.token} is probably not in {guildId}")
            return req.json()
        return req.json()

    async def getChannel(self, channelId):
        """Returns id of the server the channel is in"""
        req = await self.client.get(
            f"https://discord.com/api/v9/channels/{channelId}")
        if 'guild_id' not in req.json():
            console.f_print(f"Server ID not found.")
            guildId = input(
                f"{Fore.GREEN}{Style.BRIGHT}Please enter the server Id: {Style.RESET_ALL}")
            return guildId
        guildId = req.json()["guild_id"]
        if not guildId:
            return None
        return guildId

    async def leave(self, guildId: str):
        req = await self.client.delete(
            f"https://discord.com/api/v9/users/@me/guilds/{guildId}")
        if req.status_code != 204:
            console.f_print(f"{self.token} failed to leave server: {guildId}")
            return False
        else:
            console.s_print(f"{self.token} left server: {guildId}")
            return True
    async def getMessage(self, messageId, channelId):
        """Gets the message, returns a message object 😃"""
        req = await self.client.get(
            f"https://discord.com/api/v9/channels/{channelId}/messages?limit=1&around={messageId}")
        return req.json() 
    async def getReactions(self, messageId, channelId):
        try:
            mesasgeObject = await self.getMessage(messageId, channelId)
            mesasgeObject = mesasgeObject[0]
            reactions = list(mesasgeObject["reactions"])
            if len(reactions) == 0:
                console.f_print("Message has 0 reactions.")
                return None
            firstEmoji = reactions[0]["emoji"]
            return firstEmoji
        except Exception as e:
            console.f_print(e)
            return None
    async def addReaction(self, messageId, channelId, emojiObj):
        try:
            req = await self.client.put(
                f"https://discord.com/api/v9/channels/{channelId}/messages/{messageId}/reactions/{emojiObj}/%40me")
            if req.status_code != 204:
                console.f_print(f"{self.token} failed to bypass reaction verification.")
                return req.json()
            else:
                console.s_print(f"{self.token} successfully bypassed reaction verification.")
                return req.json()
        except Exception as e:
            return None
    async def usernameChange(self, username: str, password: str):
        req = await self.client.patch("https://discord.com/api/v9/users/@me", json={
            "password": password,
            "username": username
        })
        if req.status_code == 200:
            console.s_print(f"{self.token} Username changed to {username}")
        else:
            console.f_print(f"{self.token} Failed to change username to {username}")
    async def bioChange(self, newBio: str):
        req = await self.client.patch("https://discord.com/api/v9/users/@me", json={
            "bio": newBio
        })
        if req.status_code != 200:
            console.f_print(f"{self.token} failed to change bio to {newBio}")
        else:
            console.s_print(f"{self.token} changed bio to {newBio}")
    async def sendFriendRequest(self, username, discrim):
        req = await self.client.post("https://discord.com/api/v9/users/@me/relationships", json={
            "username": username,
            "discriminator": discrim
        })
        if req.status_code != 204:
            console.f_print(f"{self.token} Failed to send friend request to {username}#{discrim}")
            return req
        else:
            console.s_print(f"{self.token} Sent friend request to {username}#{discrim}")
            return req
from ctypes import Union
import time
from httpx import Client
global qurantinedTokens
global sentUsers
global sockStatus
global cachedSessions
sockStatus = "Open" 
cachedSessions = []
sentUsers = []
qurantinedTokens = []
blacklistedUsers = []
def getQurantinedToken(token):
    if token in getQurantinedToken:
        return "yes"
    else:
        return "no"
def qurantineToken(token):
    qurantinedTokens.append(token)
    return None
def unqurantineToken(token):
    time.sleep(600)
    for i in range(len(qurantinedTokens)):
        if qurantinedTokens[i] == token:
            qurantinedTokens.pop(i)
            return None
def getcachedsession(token): 
    for session in cachedSessions:
        if session["token"] == token:
            return session["session"]
    return None
import time
global qurantinedTokens
global sentUsers
global sockStatus
sockStatus = "Open" 
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
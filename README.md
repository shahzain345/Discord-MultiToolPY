# Discord MultiTool-PY
## By Shahzain
<li>This project was inspired by DMDGO by Vanshaj https://github.com/V4NSH4J/discord-mass-DM-GO</li>

# About
<strong>Discord Multi Tool-PY</strong> is a multi-threaded Discord Self Bot and it is used for many features such as the token joiner and MassDM

# Features
<li>Proxyless/HTTP Proxy Support</li>
<li>Token Joiner</li>
<li>Token Bio Changer</li>
<li>Token Username Changer</li>
<li>Token Format Changer [Email:Pass:Token] => [Token]</li>
<li>MassDM</li>
<li>Single DM Spam</li>
<li>Server Joiner(Captcha support)</li>
<li>Server Leaver</li>
<li>Member Scrapper</li>
<li>Username Scrapper(Soon)</li>
<li>Easy to use and setup</li>
<li>Server spammer(Has MassMention)</li>
<li>Token Checker</li>

## Config
| Name                                      | Type | Description                                                                                                                            |
|-------------------------------------------|------|----------------------------------------------------------------------------------------------------------------------------------------|
| <code>removeDeadTokens</code>             | bool | After checking MultiTool will remove all non-working tokens from input/tokens.txt                                                      |
| <code>captcha_api</code>                  | str  | The url of the captcha api you are gonna use to bypass captcha on join, capmonster.cloud and anti-captcha.com are currently supported. |
| <code>captcha_key</code>                  | str  | Your api key for captcha_api.                                                                                                          |
| <code>useDelays</code>                    | bool | If you want to use delays to avoid being rate limited and detected.                                                                    |
| <code>save_failed_logs</code>             | bool | Saves failed logs to logs/logtype.txt                                                                                                  |
| <code>bypass_membership_screening</code>  | bool | Set this to true if you want to bypass membership screening upon joining server. Setting this to true is recommended.                  |
| <code>bypass_reaction_verification</code> | bool | Set this to true if your target server has a reaction verification.                                                                    |
| <code>proxyless</code>                    | bool | If you want to use the tool without proxies.                                                                                           |
| <code>proxyProtocol</code>                | str  | Your proxy protocol, by default its http                                                                                               |

## Example Configuration
```json
{
    "removeDeadTokens": true,
    "captcha_api": "anti-captcha.com",
    "captcha_key": "your capkey",
    "useDelays": true,
    "save_failed_logs": false,
    "bypass_membership_screening": true,
    "bypass_reaction_verification": false,
    "proxyless": false,
    "proxyProtocol": "http"
}
```
## Need Help?
Join our guilded server for help: https://www.guilded.gg/i/EAJz3WY2
## How to use?
Install all the requirements
<pre><code>pip install -r requirements.txt
</code></pre>
Fill in the config.json file and message.json file<br/>
And run the main.py file
<pre><code>python main.py
</code></pre>
## Note:
Shahzain345 will not be responsible for any damage caused by this script.<br/>
If you see anyone selling this tool report it to me asap!
## Thank You!

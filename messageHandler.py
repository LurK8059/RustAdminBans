import requests
import time
import logging
import config

# Set up logging and formatting
logger = logging.getLogger()
logFormatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d")

# Set up the console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

# Set up the file handler
logFileName = "application"
fileHandler = logging.FileHandler("{}.log".format(logFileName))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# Set up logging levels
consoleHandler.setLevel(logging.INFO)
fileHandler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)


def sendEmbed(banObject, serverObject):
    for webhook in serverObject['publicWebhooks']:
        time.sleep(1)
        url = webhook
        data = {
            "username": serverObject['embedSettings']['EmbedBotName'],
            "avatar_url": serverObject['embedSettings']['EmbedAvatar']
        }
        if serverObject['embedSettings']['minifyEmbed'] == True:
            data["embeds"] = [
                {
                    "color":  serverObject['color'],
                    "title": serverObject['Name'],
                    "fields": [
                        {
                        "name": config.steam_Emoji + " Banned Player",
                        "value": "[{}](https://steamcommunity.com/profiles/{}) - {}".format(banObject['playerName'], banObject['steamID'], banObject['steamID'])
                        },
                        {
                        "name": "Reason",
                        "value": banObject['reason'],
                        "inline": True
                        },
                         {
                        "name": "\u200b",
                        "value": "\u200b",
                        "inline": True
                        },
                        {
                        "name": config.expiry_Emoji + " Expiry",
                        "value": banObject['banLength'],
                        "inline": True
                        },
                    ]
                }
            ]
        else:
            data["embeds"] = [
                {
                    "color": serverObject['color'],
                    "title": serverObject['Name'],
                    "thumbnail":
                        {
                            "url": banObject['avatar']
                        },
                    "fields": [
                        {
                        "name": "Banned Player",
                        "value": "[{}](https://steamcommunity.com/profiles/{}) - {}".format(banObject['playerName'], banObject['steamID'], banObject['steamID'])
                        },
                        {
                        "name": "Expiry",
                        "value": banObject['banLength']
                        },
                        {
                        "name": "Reason",
                        "value": banObject['reason']
                        }
                    ]
                }
            ]

        try:
            result = requests.post(url, json=data)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error("Embed failed to send with the error: {}".format(err))
        else:
            logger.info("Embed sent to {} with the response {}".format(serverObject['Name'], result.status_code))


def sendStaffEmbed(banObject, serverObject):
    for webhook in serverObject['staffWebhooks']:
        time.sleep(1)
        url = webhook
        data = {
            "username": serverObject['embedSettings']['EmbedBotName'],
            "avatar_url": serverObject['embedSettings']['EmbedAvatar']
        }
        data["embeds"] = [
                {
                    "color":  serverObject['color'],
                    "title": serverObject['Name'],
                    "thumbnail": {
                    "url": banObject['avatar'],
                    },
                    "fields": [
                        {
                        "name": "Player Information",
                        "value": "{} - {}\n\u200b".format(banObject['playerName'], banObject['steamID']),
                        "inline": False
                        },
                        {
                        "name": "Ban Information",
                        "value": "Ban Expiry: **{}**\n`{}`".format(banObject['banLength'], banObject['reason']),
                        "inline": False
                        },
                        {
                        "name": "BattleMetrics Links",
                        "value": "\n\u200b{} Ban Link: [Click here](https://www.battlemetrics.com/rcon/bans/edit/{})\n\n{} Profile: [Click here](https://www.battlemetrics.com/rcon/players/{})".format(config.battlemetrics_Emoji, banObject['banid'], config.battlemetrics_Emoji, banObject['playerDataID']),
                        "inline": True
                        },
                        {
                        "name": "Steam Links",
                        "value": "\n\u200b{} Profile: [{}](https://steamcommunity.com/profiles/{})".format(config.steam_Emoji, banObject['steamID'],banObject['steamID']),
                        "inline": True
                        },
                        {
                        "name": "Note:",
                        "value": "```{}```".format(banObject['staffBanNote']),
                        "inline": False
                        },
                    ]
                }
            ]
        
        try:
            result = requests.post(url, json=data)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error("Embed failed to send with the error: {}".format(err))
        else:
            logger.info("Embed sent to {} with the response {}".format(serverObject['Name'], result.status_code))
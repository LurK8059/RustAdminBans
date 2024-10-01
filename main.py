from discord.utils import get
import config
import messageHandler
import json
from discord.ext import commands
from discord.ext import tasks
import time
from datetime import datetime
import re
import discord
import aiohttp

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=config.command_prefix, case_insensitive=True, intents=intents)

serversArray = []
file = open('servers.json')
servers = json.load(file)

@bot.event
async def on_ready():
    # create log files if they don't exist
    for server in servers:
        file = open('bans/{}.log'.format(server['serverID']), 'a+')
        file.close

        # append servers into array
        serversArray.append(server['serverID'])

    track_bans.start()
    print("Bans Bot Online")

@tasks.loop(seconds=60)
async def track_bans():
    for server in servers:
        # load log file in array
        knownBansArray = []
        with open('bans/{}.log'.format(server['serverID']), "r") as logFile:
            for line in logFile:
                line = line.replace("\n", "")
                knownBansArray.append(line)
                logFile.close
        
        # Check to ensure Bearer is present in the auth token field
        if not server['bm_token'].startswith('Bearer '):
            bm_token = f"Bearer {server['bm_token']}"
        else:
            bm_token = server['bm_token']
            
        # make call to BM and return data
        url = "https://api.battlemetrics.com/bans"
        headers = {'content-type': 'application/json',
                   'Accept-Charset': 'UTF-8', 'Authorization': bm_token}

        async with aiohttp.ClientSession() as session:
            data = await fetch(url, headers, session)

        # loop through data and check each ban
        try:
            for ban in data['data']:
                    if ban['type'] == "ban" and ban['id'] not in knownBansArray and ban['relationships']['server']['data']['id'] == server['serverID']:
                        if not 'meta' in ban:
                            if ban['attributes']['identifiers'][0]['manual']:
                                print('Warning: Manual Ban Detected. Do not use this function: https://gyazo.com/aaa5f057c174265e69a5b17a50fe0800')
                                print('Contact your developer or the author of this bot for further support.')
                            else:
                                print('Malformed Response from Battlemetrics')
                        else:
                            banObject = {}
                            banObject['playerName'] = (ban['meta']['player'][:150] + ' (truncated)') if len(ban['meta']['player']) > 150 else ban['meta']['player']
                            for identifier in ban['attributes']['identifiers']:
                                if identifier['type'] == "steamID":
                                    banObject['steamID'] = identifier['identifier']
                                    if not (identifier.get('metadata') is None):
                                        banObject['avatar'] = identifier['metadata']['profile']['avatarmedium']
                                    else:
                                        banObject['avatar'] = "https://i.gyazo.com/2b4181769d85f5adb53694bf156d665c.png"
                            banObject['reason'] = (ban['attributes']['reason'][:2000] + ' (truncated)') if len(ban['attributes']['reason']) > 2000 else ban['attributes']['reason']
                            banObject['reason'] = banObject['reason'].replace("{", "⁍").replace("}", "⁍")
                            banObject['reason'] = banObject['reason'].replace("⁍⁍timeLeft⁍⁍", "").replace("⁍⁍duration⁍⁍", "")
                            if ban['attributes']['expires'] == None:
                                banObject['banLength'] = "Never - Perm Banned"
                            else:
                                banLength = time.strptime(
                                    ban['attributes']['expires'], "%Y-%m-%dT%H:%M:%S.%fZ")
                                banLength = time.mktime(banLength)
                                banObject['banLength'] = datetime.utcfromtimestamp(
                                    banLength).strftime('%a %b %d %Y')
                            banObject['banid'] = ban['id']
                            banObject['playerDataID'] = ban['relationships']['player']['data']['id']
                            note = ban['attributes']['note']
                            note = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", r"[Removed IP]", note)  # Remove IPs and replace with [Removed IP]
                            note = re.sub(r"<[^>]*>", r" ", note)  # Remove HTML Tags
                            banObject['staffBanNote'] = note
                            
                            messageHandler.sendEmbed(banObject, server)
                            messageHandler.sendStaffEmbed(banObject, server)
                            with open('bans/{}.log'.format(server['serverID']), "a") as logFile:
                                logFile.write('{}\n'.format(ban['id']))
                                logFile.close
        except Exception as e:
            print("Unable to process ban (BM Error) for server {} Error: {}".format(server['Name'], e))


async def fetch(url, headers, session):
    async with session.get(url, headers=headers) as response:
        res = await response.json()
        return res

bot.run(config.discord_token)

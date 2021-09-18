import asyncio
import json
import random
import os
import datetime
import discord
from uptime import boottime
import psutil
import requests

now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
loop = asyncio.get_event_loop()

def RefreshGames():
    # Open games from json
    with open("games.json") as f:
        games_list = json.load(f)
        return games_list

"""
def TextValidator(text):
    if text == "":
        return False
    return True
"""

# GAMES
def Get(author):
    if RefreshGames() == []: return "There is no game to choose from"
    rnd_game = random.choice(RefreshGames())
    print(now+author+"Generated a random game : "+rnd_game)
    return rnd_game


def Add(author, message):
    msg_list = str(message)[5:]
    if msg_list == "": return "Enter a valid name"
    with open("games.json", "r+") as file:
        data = json.load(file)
        data.append(msg_list)
        file.seek(0)
        json.dump(data, file, sort_keys=True, indent=4)

    print(now+author+"Added : "+msg_list)
    return "Added : "+msg_list


def Delete(author, message):
    msg_list = str(message)[5:]
    if msg_list == "": return "Enter a valid name"
    try:
        with open("games.json", "r+") as file:
            data = json.load(file)
            data.remove(msg_list)
            file.seek(0)
            with open("games.json", "w") as file2:
                data2 = []
                json.dump(data2, file2, sort_keys=True, indent=4)
            json.dump(data, file, sort_keys=True, indent=4)
    except Exception as e:
        print(e)
        return "There is no game called "+msg_list
    else:
        print(now+author+"Deleted : "+msg_list)
        return "Deleted : "+msg_list


def Reset(author):
    with open("games.json", "w") as file:
        data = []
        json.dump(data, file, sort_keys=True, indent=4)
    print(now+author+"Resetted all games")
    return "Resetted games"


def List(author):
    if RefreshGames() == []: return "There is no game to choose from"
    print(now+author+"Listed all the games")
    return '\n'.join(str(x) for x in RefreshGames())



# CHANNELS
async def Clean(author, m, client):
    temp = []
    async for msg in m.channel.history(limit=10000):
        if author == client.user or msg.content.startswith('$'):
            temp.append(msg)

        if len(temp) == 20:
            try:
                await m.channel.delete_messages(temp)
            except Exception as e:
                print(e)
                return "Cannot delete messages older than 14 days"

    print(now+author+"Deleted all chat record for and by bot")
    return ("Delete successful")


# MISC
def Status(author):
    # Get system info
    uptime = str(boottime())
    LoadCPU = str(psutil.cpu_percent())
    VMEM = str(psutil.virtual_memory()[2])
    print(now+author+"Asked for status")
    return(
        "Up since : "+uptime
        + "\nCPU Load : "+LoadCPU
        + '\nMemory % used: '+VMEM
    )

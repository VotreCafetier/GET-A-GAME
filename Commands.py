import asyncio, json, random, os, datetime, discord, psutil, requests
from uptime import boottime

now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")

def refresh_games() -> list[str]:
    # Open games from json
    with open("games.json") as f:
        games_list = json.load(f)
        return games_list

# GAMES
def get_game(author:str) -> str:
    if refresh_games() == []:
        return "There is no game to choose from"
    rnd_game = random.choice(refresh_games())
    print(now+author+"Generated a random game : "+rnd_game)
    return rnd_game


def add_game(author:str, message:str) -> str:
    msg_list = str(message)[5:]
    if msg_list == "":
        return "Enter a valid name"
    with open("games.json", "r+") as file:
        data = json.load(file)
        data.append(msg_list)
        file.seek(0)
        json.dump(data, file, sort_keys=True, indent=4)

    print(now+author+"Added : "+msg_list)
    return "Added : "+msg_list


def delete_game(author:str, message:str) -> str:
    msg_list = str(message)[5:]
    if msg_list == "":
        return "Enter a valid name"
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


def reset_games(author:str) -> str:
    with open("games.json", "w") as file:
        data = []
        json.dump(data, file, sort_keys=True, indent=4)
    print(now+author+"Resetted all games")
    return "Resetted games"


def list_games(author:str) -> str:
    if refresh_games() == []: return "There is no game to choose from"
    print(now+author+"Listed all the games")
    z = ''
    for idx, val in enumerate(refresh_games()): z += (f'[{idx}] {val}\n')
    return z


# CHANNELS
async def clean(author:str, m:discord.message, client:discord.client) -> str:
    temp = []
    async for msg in m.channel.history(limit=10000):
        if msg.author == client.user or msg.content.startswith('$'):
            temp.append(msg)

        if len(temp) == 20:
            try:
                await m.channel.delete_messages(temp)
            except Exception as e:
                print(e)
                break

    # if there is still message, bruteforce
    async for msg in m.channel.history(limit=10000):
        if msg.author == client.user or msg.content.startswith('$'):
            try:
                await msg.delete()
            except Exception as e:
                print(e)
                continue

    print(now+author+"Deleted all chat record for and by bot")
    return ("Delete successful")


# MISC
def status(author:str) -> str:
    uptime = str(boottime())
    LoadCPU = str(psutil.cpu_percent())
    VMEM = str(psutil.virtual_memory()[2])
    print(now+author+"Asked for status")
    return(
        "Up since : "+uptime
        + "\nCPU Load : "+LoadCPU
        + '\nMemory % used: '+VMEM
    )

import json, random, datetime, discord, psutil, logging
from pathlib import Path

now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
FILENAME = Path("games.json")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get games from games.json
def get_games() -> list[str]:
    games_list = []
    try:
        with open(FILENAME) as f:
            games_list = json.load(f)
    except FileNotFoundError:
        with open(FILENAME, 'w') as f:
            json.dump(games_list, f, indent=4)

    return games_list


def get_rnd_game(author:str) -> str:
    games_list = get_games()
    if not games_list:
        return "There is no game to choose from"
    rnd_game = random.choice(games_list)
    logger.info(f"{now}{author} Generated a random game: {rnd_game}")
    return rnd_game


def add_game(author:str, message:str) -> str:
    msg_list = message
    if msg_list == "":
        return "Enter a valid name"
    with FILENAME.open("r+") as file:
        data = json.load(file)
        data.append(msg_list)
        file.seek(0)
        json.dump(data, file, sort_keys=True, indent=4)

    logger.info(f"{now}{author} Added: {msg_list}")
    return f"Added: {msg_list}"


def delete_game(author:str, message:str) -> str:
    msg_list = message
    if msg_list == "":
        return "Enter a valid name"
    try:
        with FILENAME.open("r+") as file:
            data = json.load(file)
            if msg_list not in data:
                raise ValueError
            data.remove(msg_list)
            file.seek(0)
            json.dump(data, file, sort_keys=True, indent=4)
    except ValueError:
        return f"There is no game called {msg_list}"
    else:
        logger.info(f"{now}{author} Deleted: {msg_list}")
        return f"Deleted: {msg_list}"


def reset_games(author:str) -> str:
    with FILENAME.open("w") as file:
        data = []
        json.dump(data, file, sort_keys=True, indent=4)
    logger.info(f"{now}{author} Resetted all games")
    return "Resetted games"


def list_games(author:str) -> str:
    games = get_games()
    if not games:
        return "There is no game to choose from"
    
    games_list = '\n'.join([f"[{idx}] {val}" for idx, val in enumerate(games)])
    logger.info(f"{now,author} Listed all the games")
    return games_list


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
                logging.error(e)
                break

    # if there is still message, bruteforce
    async for msg in m.channel.history(limit=10000):
        if msg.author == client.user or msg.content.startswith('$'):
            try:
                await msg.delete()
            except Exception as e:
                logging.error(e)
                continue

    logging.info(now+author+"Deleted all chat record for and by bot")
    return ("Delete successful")


# MISC
async def status(author:str) -> str:
    uptime = psutil.boot_time()
    LoadCPU = psutil.cpu_percent()
    VMEM = psutil.virtual_memory()[2]
    logger.info(now+author+"Asked for status")
    return(
        "Up since : "+uptime
        + "\nCPU Load : "+LoadCPU
        + '\nMemory % used: '+VMEM
    )

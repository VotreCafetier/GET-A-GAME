import json, random, discord, psutil, logging, aiofiles
from pathlib import Path

FILEPATH = Path("games.json")

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Get games from games.json
async def get_games() -> list[str]:
    games_list: List[str] = []

    if not FILEPATH.exists():
        async with aiofiles.open(FILEPATH, 'w') as f:
            await f.write(json.dumps(games_list, indent=4))
    else:
        async with aiofiles.open(FILEPATH, "r") as f:
            games_list = json.loads(await f.read())

    return games_list


async def get_rnd_game(author: str) -> str:
    games_list = await get_games()
    if not games_list:
        return "There is no game to choose from"
    rnd_game = random.choice(games_list)
    logger.info(f"[{author}] Generated a random game: {rnd_game}")
    return rnd_game


async def add_game(author: str, message: str) -> str:
    msg_list = message
    if msg_list == "":
        return "Enter a valid name"
    async with aiofiles.open(FILEPATH, "r+") as file:
        data = json.loads(await file.read())
        data.append(msg_list)
        file.seek(0)
        await file.write(json.dumps(data, sort_keys=True, indent=4))

    logger.info(f"[{author}] Added: {msg_list}")
    return f"Added: {msg_list}"


async def delete_game(author: str, message: str) -> str:
    msg_list = message
    if msg_list == "":
        return "Enter a valid name"
    try:
        async with aiofiles.open(FILEPATH, "r+") as file:
            data = json.loads(await file.read())
            if msg_list not in data:
                raise ValueError
            data.remove(msg_list)
            file.seek(0)
            await file.write(json.dumps(data, sort_keys=True, indent=4))
    except ValueError:
        return f"There is no game called {msg_list}"
    else:
        logger.info(f"[{author}] Deleted: {msg_list}")
        return f"Deleted: {msg_list}"


async def reset_games(author: str) -> str:
    async with aiofiles.open(FILEPATH, "w") as file:
        data = []
        await file.write(json.dumps(data, sort_keys=True, indent=4))
    logger.info(f"[{author}] Resetted all games")
    return "Resetted games"


async def list_games(author: str) -> str:
    games = await get_games()
    if not games:
        return "There is no game to choose from"
    
    games_list = '\n'.join([f"[{idx}] {val}" for idx, val in enumerate(games)])
    logger.info(f"[{author}] Listed all the games")
    return games_list


# CHANNELS
async def clean(author: str, m:discord.message, client:discord.client) -> str:
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

    logging.info(f"[{author}] Deleted all chat record for and by bot")
    return ("Delete successful")


# MISC
async def status(author: str) -> str:
    uptime = psutil.boot_time()
    LoadCPU = psutil.cpu_percent()
    VMEM = psutil.virtual_memory()[2]
    logger.info(f"[{author}] Asked for status")
    return(
        f'Up since : {uptime}\nCPU Load : {LoadCPU}\nMemory % used: {VMEM}'
    )

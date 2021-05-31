import random
import discord
import json
import datetime
from secrets import discord_token
from uptime import boottime

client = discord.Client()
now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")


def RefreshGames():
    # Open games from json
    with open('games.json') as f:
        games_list = json.load(f)
        return games_list


def TextValidator(text):
    if text == "":
        return False
    return True


@client.event
async def on_ready():
    print(now+'We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg_author = str(message.author)+" "
    # Prevent the bot to reply to itself
    if message.author == client.user:
        return

    # Generate a random games
    if message.content.startswith('$Get'):
        try:
            rnd_game = random.choice(RefreshGames())
            print(now+msg_author+"Generated a random game : "+rnd_game)
            await message.channel.send(rnd_game)
        except Exception as e:
            print(e)
            await message.channel.send(now+"There is no game to choose from")
        return

    # List all of the games
    if message.content.startswith('$List'):
        try:
            print(now+msg_author+"Listed all the games")
            await message.channel.send('\n'.join(str(x) for x in RefreshGames()))
        except Exception as e:
            print(e)
            await message.channel.send("There is no game to choose from")
        return

    # Add an element to the game array
    if message.content.startswith('$Add'):
        msg_list = str(message.content)[5:]
        if TextValidator(msg_list) is False:
            await message.channel.send("Enter a valid name")
            return

        with open("games.json", "r+") as file:
            data = json.load(file)
            data.append(msg_list)
            file.seek(0)
            json.dump(data, file, sort_keys=True, indent=4)

        print(now+msg_author+"Added : "+msg_list)
        await message.channel.send("Added : "+msg_list)
        return

    # delete game
    if message.content.startswith('$Del'):
        msg_list = str(message.content)[5:]
        if TextValidator(msg_list) is False:
            await message.channel.send("Enter a valid name")
            return
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
            await message.channel.send("There is no game called "+msg_list)
        else:
            print(now+msg_author+"Deleted : "+msg_list)
            await message.channel.send("Deleted : "+msg_list)
        return

    # reset all games
    if message.content.startswith('$Reset'):
        with open("games.json", "w") as file:
            data = []
            json.dump(data, file, sort_keys=True, indent=4)
        print(now+msg_author+"Resetted all games")
        await message.channel.send("Resetted games")
        return

    # Help : Shows all the commands
    if message.content.startswith('$Help'):
        await message.channel.send(
            "Here is the list of all the commands :\n\n"
            "$Get : Generate a random game from the list\n"
            "$List : Listing all the games\n"
            "$Add : Add a specified game\n"
            "$Reset : Delete all the games\n"
            "$Del : Delete a specified game\n"
            "$Clean : Clean all of the bot chat history\n"
            "$Status : Show status of servers"
        )
        return

    # Clean : delete all message sent from bot
    if message.content.startswith('$Clean'):
        await message.channel.send("Cleaning started")
        async for msg in message.channel.history(limit=10000):
            if msg.author == client.user:
                try:
                    await msg.delete()
                except Exception as e:
                    print(e)

        await message.channel.send("Delete successful")
        print(now+msg_author+"Deleted all chat record of bot")
        return

    # Status : Get system up time
    if message.content.startswith('$Status'):
        print(now+msg_author+"Asked for status")
        await message.channel.send("Up since : "+str(boottime()))
        return

    await message.channel.send("There is no command")

try:
    client.run(discord_token)
except Exception as e:
    print(e)

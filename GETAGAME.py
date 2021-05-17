import random
import discord
import json
import datetime

token = "NDY5NTkwODM4NjM3NDk0Mjc0.W1DqjA.oyh7oyUOQxWeAHAB3lNkJe9_eLo"
client = discord.Client()
now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")


def RefreshGames():
    # Open games from json
    with open('games.json') as f:
        games_list = json.load(f)
        return games_list


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

    # List all of the games
    if message.content.startswith('$List'):
        try:
            print(now+msg_author+"Listed all the games")
            await message.channel.send('\n'.join(str(x) for x in RefreshGames()))
        except Exception as e:
            print(e)
            await message.channel.send("There is no game to choose from")

    # Add an element to the game array
    if message.content.startswith('$Add'):
        msg_list = str(message.content)[5:]
        with open("games.json", "r+") as file:
            data = json.load(file)
            data.append(msg_list)
            file.seek(0)
            json.dump(data, file)

        print(now+msg_author+"Added : "+msg_list)
        await message.channel.send("Added : "+msg_list)

    # delete game
    if message.content.startswith('$Del'):
        msg_list = str(message.content)[5:]
        try:
            with open("games.json", "r+") as file:
                data = json.load(file)
                data.remove(msg_list)
                file.seek(0)
                with open("games.json", "w") as file2:
                    data2 = []
                    json.dump(data2, file2)
                json.dump(data, file)
        except Exception as e:
            print(e)
            await message.channel.send("There is no game called "+msg_list)
        else:
            print(now+msg_author+"Deleted : "+msg_list)
            await message.channel.send("Deleted : "+msg_list)

    # reset all games
    if message.content.startswith('$Reset'):
        with open("games.json", "w") as file:
            data = []
            json.dump(data, file)
        print(now+msg_author+"Resetted all games")
        await message.channel.send("Resetted games")

    # Help : Shows all the commands
    if message.content.startswith('$Help'):
        await message.channel.send(
            "Here is the list of all the commands :\n\n"
            "$Get : Generate a random game from the list\n"
            "$List : Listing all the games\n"
            "$Reset : Delete all the games\n"
            "$Add : Add a specified game\n"
            "$Del : Delete a specified game\n"
        )

try:
    client.run(token)
except Exception as e:
    print(e)

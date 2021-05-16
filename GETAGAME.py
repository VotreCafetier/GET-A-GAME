import random
import discord
import json

token = "NDY5NTkwODM4NjM3NDk0Mjc0.W1DqjA.oyh7oyUOQxWeAHAB3lNkJe9_eLo"
client = discord.Client()


def RefreshGames():
    # Open games from json
    with open('games.json') as f:
        games_list = json.load(f)
        return games_list


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Prevent the bot to reply to itself
    if message.author == client.user:
        return

    # Generate a random games
    if message.content.startswith('$Get'):
        try:
            rnd_game = random.choice(RefreshGames())
            print("Generated a "+rnd_game)
            await message.channel.send(rnd_game)
        except Exception as e:
            print(e)
            await message.channel.send("There is no game to choose from")

    # List all of the games
    if message.content.startswith('$List'):
        try:
            print("Printed List")
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

        RefreshGames()
        print("Added : "+msg_list)
        await message.channel.send("Added : "+msg_list)

    # reset array
    if message.content.startswith('$Reset'):
        with open("games.json", "w") as file:
            data = []
            json.dump(data, file)

        RefreshGames()
        print("Resetted games")
        await message.channel.send("Resetted games")

    # Delete a game

try:
    client.run(token)
except Exception as e:
    print(e)

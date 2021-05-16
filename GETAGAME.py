import random
import discord
import json

token = "NDY5NTkwODM4NjM3NDk0Mjc0.W1DqjA.oyh7oyUOQxWeAHAB3lNkJe9_eLo"
client = discord.Client()

# Open games from json
with open('games.json') as f:
    games_list = json.load(f)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # Prevent the bot to reply to itself
    if message.author == client.user:
        return

    # Generate a random games
    if message.content.startswith('$Gen'):
        await message.channel.send(random.choice(games_list))

    # List all of the array
    if message.content.startswith('$List'):
        for games in games_list:
            await message.channel.send(games, end = "\n")

    # Add an element to the game array
    if message.content.startswith('$Add'):
        msg_list = str(message.content)[5:]
        #RENDU ICI
        with open("games.json", "r+") as file:
            data = json.load(file)
            data.update(msg_list)
            file.seek(0)
            json.dump(data, file)


        games_list.append(msg_list)

        print("Added : "+msg_list)
        # games.list.append(message)
        await message.channel.send("Added : "+msg_list)

    #reset array

try:
    client.run(token)
except Exception as e:
    print(e)

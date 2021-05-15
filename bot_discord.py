import random
import discord


api_token = "NDY5NTkwODM4NjM3NDk0Mjc0.W1DqjA.oyh7oyUOQxWeAHAB3lNkJe9_eLo"

games_list = [
"Battlefield 4",
"Dead By Daylight",
"Starcraft 2",
"Minecraft",
"Tom Clancy's Rainbow Six Siege",
"Halo: The Master Chief Collection",
"Totally Accurate Battlegrounds",
"Osu!",
"Overwatch",
"Escape From Tarkov"
]

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$Gen'):
        await message.channel.send(random.choice(games_list))

    if message.content.startswith('$List'):
        for games in games_list:
            await message.channel.send(games)


client.run(api_token)

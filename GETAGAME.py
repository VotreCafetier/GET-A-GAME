import random, os, discord, json, datetime, psutil, requests
from uptime import boottime

# Files import
from Commands import *
import secrets


client = discord.Client(intents=discord.Intents.default())


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
        await message.channel.send(get_game(msg_author))
        return

    # List all of the games
    if message.content.startswith('$List'):
        await message.channel.send(list_games(msg_author))
        return

    # Add an element to the game array
    if message.content.startswith('$Add'):
        await message.channel.send(add_game(msg_author, message.content))
        return

    # delete game
    if message.content.startswith('$Del'):
        await message.channel.send(delete_game(msg_author, message.content))
        return

    # reset all games
    if message.content.startswith('$Reset'):
        await message.channel.send(reset_games(msg_author))
        return

    # Help : Shows all the commands
    if message.content.startswith('$Help'):
        await message.channel.send(
            "Here is the list of all the commands :\n"
            "--- Games ---\n"
            "$Get : Generate a random game from the list\n"
            "$List : Listing all the games\n"
            "$Add : Add a specified game\n"
            "$Reset : Delete all the games\n"
            "$Del : Delete a specified game\n\n"
            "--- Misc ---\n"
            "$Clean : Clean all of the bot chat history\n"
            "$Status : Show status of servers"
        )
        return

    # Clean : delete all message sent from bot
    if message.content.startswith('$Clean'):
        await message.channel.send("Cleaning started")
        await message.channel.send(await clean(msg_author, message, client))
        return

    #  Status : Get system up time
    if message.content.startswith('$Status'):
        await message.channel.send(status(msg_author))
        return

    # Default value if no command
    if message.content.startswith('$'):
        await message.channel.send("There is no command")

try:
    client.run(secrets.discord_token)
except Exception as e:
    print(e)

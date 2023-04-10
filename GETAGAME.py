import discord, logging
from discord.ext import commands

# Files import
from Commands import *
import secrets


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')

@bot.command()
async def get(ctx):
    await ctx.send(await get_rnd_game(str(ctx.author)))

@bot.command(name='list')
async def _list(ctx):
    await ctx.send(await list_games(str(ctx.author)))

@bot.command()
async def add(ctx, game):
    await ctx.send(await add_game(str(ctx.author), game))

@bot.command(name='del')
async def _del(ctx, game):
    await ctx.send(delete_game(str(ctx.author), game))

@bot.command()
async def reset(ctx):
    await ctx.send(await reset_games(str(ctx.author)))
""" 
@bot.command()
async def help(ctx):
    await ctx.send(
        "Here is the list of all the commands :\n"
        "--- Games ---\n"
        "$get : Generate a random game from the list\n"
        "$list : Listing all the games\n"
        "$add : Add a specified game\n"
        "$reset : Delete all the games\n"
        "$del : Delete a specified game\n\n"
        "--- Misc ---\n"
        "$clean : Clean all of the bot chat history\n"
        "$status : Show status of servers"
    ) """

@bot.command()
async def clean(ctx):
    await ctx.send("Cleaning started")
    await ctx.send(clean(str(ctx.author), ctx.message, bot))

@bot.command()
async def status(ctx):
    await ctx.send(status(ctx.author))

try:
    bot.run(secrets.discord_token)
except Exception as e:
    logging.error(e)
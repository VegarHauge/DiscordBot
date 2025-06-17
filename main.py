import os
import logging
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
#from champions.py import Champions
import random
from Commands.brawl import brawl_func

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')

@bot.command()
async def brawl(ctx):
    await brawl_func(ctx)


@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if channel.name == "general":
            await channel.send(f'Thomas har smuglet inn {member.name}, håper du har visum på plass!')
            break





bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)


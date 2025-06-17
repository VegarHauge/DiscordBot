import os
import logging
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

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

@bot.event
async def on_member_join(member, ctx):
    await ctx.send(f'Thomas har smuglet inn {member.name}, håper du har visum på plass.')

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")



bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)


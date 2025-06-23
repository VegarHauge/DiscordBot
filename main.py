import os
import logging
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import pomice

from Commands.blackjack import Blackjack
from Commands.brawl import brawl_func
from Commands.helloTeam import play_greeting_sound
from Commands.music import Music
from Commands.lola import LolaCog
from Commands.minecraftCordinates import MinecraftCoordinates

from Commands.Lolalytics.build import get_build
from Commands.Lolalytics.skillOrder import get_skill_order
from Commands.Lolalytics.startingItems import get_starting_items
from Commands.Lolalytics.coreBuild import get_core_build
from Commands.Lolalytics.runes import get_runes
from Commands.Lolalytics.lateGameItems import get_late_game_items
from Commands.Lolalytics.summoners import get_summoner

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configures logging globally
logging.basicConfig(
    level=logging.DEBUG,
    filename='discord.log',
    encoding='utf-8',
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True
intents.voice_states = True


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!', intents=intents
        )

    async def setup_hook(self):
        # Proper place to add cogs in discord.py 2.x
        await self.add_cog(Music(self))
        await self.add_cog(Blackjack(self))
        await self.add_cog(MinecraftCoordinates(self))
        #await self.add_cog(LolaCog(self))
        self.add_command(brawl)
        self.add_listener(on_member_join)
        self.add_listener(on_voice_state_update)
        self.add_command(lola)


    async def on_ready(self) -> None:
        print('------------')
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------------')
        await self.cogs['Music'].start_nodes()


@commands.command()
async def brawl(ctx):
    await brawl_func(ctx)

async def on_member_join(member):
    for channel in member.guild.text_channels:
        if channel.name == "general":
            await channel.send(f'Thomas har smuglet inn {member.name}, håper du har visum på plass!')
            break

async def on_voice_state_update(member, before, after):
    bot = member._state._get_client()  # or keep a global bot variable, or pass as needed
    await play_greeting_sound(member, before, after, bot)


@commands.command()
async def lola(ctx):
    print()
    build = get_build(f"{ctx.message.content.split(' ')[1]}")
    await ctx.author.send(build)


if __name__ == "__main__":
    bot = MyBot()
    bot.run(TOKEN)
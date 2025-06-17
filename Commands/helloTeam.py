import discord
import os
from dotenv import load_dotenv
import asyncio
# Path to your sound file
#SOUND_FILE = "HelloTeam.mp3"
load_dotenv()
SOUND_FILE = os.getenv('SOUND_FILE')  # Default to HelloTeam.mp3 if not set in .env

async def play_greeting_sound(member, before, after, bot):

    if (before.channel is None and after.channel is not None
        and not member.bot
        and not any(vc.channel == after.channel for vc in bot.voice_clients)):
        channel = after.channel
        voice = await channel.connect()
        audio_source = discord.FFmpegPCMAudio(SOUND_FILE)

        def after_playing(error):
            coro = voice.disconnect()
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f'Error disconnecting: {e}')

        voice.play(audio_source, after=after_playing)
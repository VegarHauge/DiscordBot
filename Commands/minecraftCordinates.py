import discord
from discord.ext import commands
import os
import json

DATA_FILE = 'mc_coordinates.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class MinecraftCoordinates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    def get_guild_data(self, guild_id):
        guild_id = str(guild_id)
        if guild_id not in self.data:
            self.data[guild_id] = {}
        return self.data[guild_id]

    def save(self):
        save_data(self.data)

    @commands.command(name='mc')
    async def mc(self, ctx, place: str = None, *args):
        guild_id = str(ctx.guild.id)
        server_data = self.get_guild_data(guild_id)

        if place is None:
            await ctx.send("Use `!mc help` for command usage.")
            return

        if place.lower() == "help":
            help_message = (
                "**Minecraft Coordinates Bot Help**\n"
                "`!mc {place}` - Show coordinates of a place.\n"
                "`!mc {place} {coordinates}` - Set or update coordinates for a place.\n"
                "place can be any name you choose, but must be one word, use _ or - instead of spaces\n"
                "`!mc all` - Show all saved places with coordinates.\n"
                "`!mc delete {place}` - Delete a saved place.\n"
                "`!mc help` - Show this help message.\n\n"
                "**Examples:**\n"
                "`!mc base 100 64 -300`\n"
                "`!mc base`\n"
                "`!mc all`\n"
                "`!mc delete base`"
            )
            try:
                await ctx.author.send(help_message)
            except discord.Forbidden:
                await ctx.send("❌ I couldn't send you a DM. Please check your privacy settings.")
            return

        if place.lower() == "all":
            if not server_data:
                await ctx.send("No coordinates saved for this server.")
                return
            entries = [f"**{key}**: {val}" for key, val in server_data.items()]
            await ctx.send("\n".join(entries))
            return

        if place.lower() == "delete":
            if len(args) != 1:
                await ctx.send("Usage: `!mc delete {place}`")
                return
            target = args[0]
            if target in server_data:
                del server_data[target]
                self.save()
                await ctx.send(f"Deleted coordinates for `{target}`.")
            else:
                await ctx.send(f"No coordinates found for `{target}`.")
            return

        if not args:
            # Show coordinates
            if place in server_data:
                await ctx.send(f"Coordinates for `{place}`: {server_data[place]}")
            else:
                await ctx.send(f"No coordinates saved for `{place}`.")
        else:
            # Set coordinates
            coordinates = ' '.join(args)
            server_data[place] = coordinates
            self.save()
            await ctx.send(f"Set coordinates for `{place}`: {coordinates}")

import discord
from discord.ext import commands
import pomice

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.pomice = pomice.NodePool()
        self.queue = {}

    # REMOVE cog_load and any self.pomice.create_node
    async def start_nodes(self):
        await self.pomice.create_node(
            bot=self.bot,
            host="localhost",
            port=2333,
            password="youshallnotpass",
            identifier="MAIN",
        )
        print(f"Node is ready!")

    async def join_and_play(self, ctx, search: str):
        voice = getattr(ctx.author, "voice", None)
        if not voice or not voice.channel:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        if not ctx.voice_client:
            await voice.channel.connect(cls=pomice.Player)

        player: pomice.Player = ctx.voice_client
        results = await player.get_tracks(query=search)

        if not results:
            await ctx.send("No results were found for that search term.")
            return

        if ctx.guild.id not in self.queue:
            self.queue[ctx.guild.id] = []

        if isinstance(results, pomice.Playlist):
            self.queue[ctx.guild.id].extend(results.tracks)
            await ctx.send(f"Added playlist `{results.name}` with {len(results.tracks)} tracks to the queue.")
        else:
            self.queue[ctx.guild.id].extend(results)
            await ctx.send(f"Added {results[0].title} to the queue.")

        if not player.is_playing:
            await self.start_next(ctx)

    @commands.command(name="play")
    async def play(self, ctx, *, search: str) -> None:
        await self.join_and_play(ctx, search)

    async def start_next(self, ctx):
        player: pomice.Player = ctx.voice_client
        q = self.queue.get(ctx.guild.id, [])
        if not q:
            await ctx.send("Queue is empty.")
            return
        track = q.pop(0)
        await player.play(track)
        await ctx.send(f"Now playing: {track.title}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        player: pomice.Player = ctx.voice_client
        if player.is_playing:
            await player.stop()
            await ctx.send("Skipped!")
            await self.start_next(ctx)
        else:
            await ctx.send("Nothing is playing.")

    @commands.command(name="queue")
    async def queue_(self, ctx):
        q = self.queue.get(ctx.guild.id, [])
        if not q:
            await ctx.send("Queue is empty.")
            return
        msg = "\n".join(f"{idx+1}. {t.title}" for idx, t in enumerate(q))
        await ctx.send(f"Current queue:\n{msg}")

    @commands.command(name="pause")
    async def pause(self, ctx):
        player: pomice.Player = ctx.voice_client
        if player.is_playing:
            await player.set_pause(True)
            await ctx.send("Paused!")
        else:
            await ctx.send("Nothing is playing.")

    @commands.command(name="resume")
    async def resume(self, ctx):
        player: pomice.Player = ctx.voice_client
        # Pomice does not have is_paused property, so just call set_pause(False)
        await player.set_pause(False)
        await ctx.send("Resumed!")

    @commands.command(name="stop")
    async def stop(self, ctx):
        player: pomice.Player = ctx.voice_client
        await player.disconnect()
        self.queue[ctx.guild.id] = []
        await ctx.send("Stopped and cleared the queue.")

async def setup(bot):
    await bot.add_cog(Music(bot))
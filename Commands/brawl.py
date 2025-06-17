import random
from champions import champion_names


async def brawl_func(ctx):
    # Check if the author is in a voice channel
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        members = [m for m in channel.members if not m.bot]
        if len(members) > len(champion_names):
            await ctx.send("Not enough champions for everyone in the channel!")
            return

        champions = random.sample(champion_names, k=len(members))
        assignments = [f"{member.mention} - {champion}" for member, champion in zip(members, champions)]
        message = "**Brawl assignments:**\n" + "\n".join(assignments)
        await ctx.send(message)
    else:
        await ctx.send("You need to be in a voice channel to use this command.")
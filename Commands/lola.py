
import discord
from discord.ext import commands
from discord import app_commands
from champions import champion_names
from Commands.Lolalytics.build import get_build

class LolaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="lola", description="Get build for a champion")
    @app_commands.describe(champion="Champion name")
    async def lola(self, interaction: discord.Interaction, champion: str):
        build = get_build(champion)
        await interaction.user.send(str(build))
        await interaction.response.send_message(f"Build sent for {champion}!", ephemeral=True)

    @lola.autocomplete('champion')
    async def champion_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=champ, value=champ)
            for champ in champion_names if current.lower() in champ.lower()
        ][:25]

async def setup(bot):
    await bot.add_cog(LolaCog(bot))
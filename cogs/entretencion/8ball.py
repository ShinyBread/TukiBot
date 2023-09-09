import discord
import random
from discord.ext import commands
from discord import app_commands
from respuestas_ochoball import respuestasOchoBall

class ochoball(commands.Cog):
    def __init__(self, TukiBot:commands.Bot) -> None:
        self.TukiBot=TukiBot
    
    @app_commands.command(
            name="8ball", 
            description='Haceme una pregunta tipo si o no y vere que te contesto'
            )
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.user.id))
    
    async def ochoball(self, interaction: discord.Interaction, *, pregunta: str):
        embed = discord.Embed(title=f'Pregunta: {pregunta}\n TukiBot dice: {random.choice(respuestasOchoBall)}')
        await interaction.response.send_message(embed=embed)

async def setup(TukiBot: commands.Bot) -> None:
    await TukiBot.add_cog(ochoball(TukiBot))
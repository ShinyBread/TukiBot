import discord
from discord.ext import commands
from discord import app_commands

class paico(commands.Cog):
    def __init__(self, TukiBot:commands.Bot) -> None:
        self.TukiBot=TukiBot
    
    @app_commands.command(
        name= 'flore',
        description= 'a la flore le gusta el paico'
    )
    async def paico(self, interaction: discord.Interaction):
        member = None
        if member == None:
            member = interaction.user
        if member.id == 227235618520956928:
            embed=discord.Embed(title="A la flore le gusta el paico")
            await interaction.response.send_message(embed=embed)

async def setup(TukiBot: commands.Bot) -> None:
    await TukiBot.add_cog(paico(TukiBot))

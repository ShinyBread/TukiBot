import discord
from discord.ext import commands
from discord import app_commands

class avatar(commands.Cog):
    def __init__(self, TukiBot:commands.Bot) -> None:
        self.TukiBot=TukiBot

    @app_commands.command(
            name='avatar', 
            description='Muestra avatar del usuario'
            )
    async def mostrar_avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None:
            member = interaction.user
        
        embed = discord.Embed(title=f'Avatar de {member.name}')
        embed.set_image(url=member.avatar)
        await interaction.response.send_message(embed=embed)

async def setup(TukiBot: commands.Bot) -> None:
    await TukiBot.add_cog(avatar(TukiBot))
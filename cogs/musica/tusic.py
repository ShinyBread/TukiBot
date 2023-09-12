import discord
from discord.ext import commands
from discord import app_commands
import youtube_dlc
from collections import deque

class tusic(commands.Cog):
    def __init__(self, TukiBot:commands.Bot) -> None:
        self.TukiBot = TukiBot
        self.queue = deque()

    @app_commands.command(
            name='play', 
            description='MUSICA TITO !'
            )
    async def play(self, interaction: discord.Interaction, url : str = None):
        if url is None:
            if len(self.queue) == 0:
                await interaction.response.send_message("Sin temazos en la cola")
                return
            else:
                url = self.queue.popleft()

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio', 'verbose': True}
        
        guild = interaction.guild
        vc = guild.voice_client

        if not vc or not vc.is_playing():
            with youtube_dlc.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **FFMPEG_OPTIONS), after=lambda e: self.bot.loop.create_task(self.play_next(guild)))
                embed = discord.Embed(title="TukiBot puso el temazo: ", description=info['title'], color=discord.Color.green())
                embed.set_thumbnail(url=info['thumbnail'])
                await interaction.response.send_message(embed=embed)
        else:
            with youtube_dlc.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                self.queue.append(url)
                embed = discord.Embed(title= 'Se agrego a la cola :', description=info['title'], color= discord.Color.blue())
                embed.set_thumbnail(url=info['thumbnail'])
                await interaction.response.send_message(embed=embed)

    async def play_next(self, guild):
        if len(self.queue) > 0 and guild.voice_client and not guild.voice_client.is_playing():
            next_url = self.queue.popleft()
            await self.play(guild, next_url)


    @app_commands.command(
            name='stop', 
            description='PARA LA MUSICA TITOOOO'
            )
    async def stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            embed = discord.Embed(title="Alguien detuvo la fiesta", color= discord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="No hay musica reproduciendose", color= discord.Color.red())
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name='join', 
            description='TukiBot entra al vc'
            )
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            embed = discord.Embed(title="{} entra al vc primero, BREA".format(interaction.user.name), color= discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return
        else:
            channel = interaction.user.voice.channel
        await channel.connect()
        embed = discord.Embed(title="TukiBot va empezar la fiesta!", color= discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name='leave', 
            description='Chao noma, TukiBot'
            )
    async def leave(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            embed = discord.Embed(title="Echaron a TukiBot, son fomes cabros... ", color= discord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="TukiBot no ta en ningun vc", color= discord.Color.red())
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name='skip', 
            description='Saltate una cancion'
            )
    async def skip(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            embed = discord.Embed(title="Saltando temazo...", color= discord.Color.yellow())
            await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(title="No hay temazos para saltar", color= discord.Color.red())
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name='queue', 
            description='Muestra los temazos en la cola'
            )
    async def queue(self, interaction: discord.Interaction):
        if len(self.queue) == 0:
            await interaction.response.send_message("No hay temazos en la cola")
        else:
            queue_list = "\n".join([f"{i+1}. {url}" for i, url in enumerate(self.queue)])
            embed = discord.Embed(title="Temazos en la cola:", description=queue_list, color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)

async def setup(TukiBot: commands.Bot) -> None:
    await TukiBot.add_cog(tusic(TukiBot))
import discord
from discord.ext import commands
from discord import app_commands
import youtube_dlc
from collections import deque


class tusic(commands.Cog):
    def __init__(self, TukiBot:commands.Bot)-> None:
        self.TukiBot = TukiBot

        self.is_playing = False
        self.is_paused = False
        self.music_queue = deque()
        self.YDL_OPTIONS = {'format': 'bestaudio', 'verbose': True}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = None

    def get_yt_video_info(self, url):
        with youtube_dlc.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title'], 'thumbnail': info.get('thumbnail')}
    
    def play_next(self):
        if len(self.music_queue)>0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e:self.play_next())
        else:
            self.is_playing= False
    
    async def play_music(self, interaction : discord.Interaction):
        if len(self.music_queue)>0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    embed = discord.Embed(title="No se pudo conectar al vc",color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.music_queue.popleft()
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    @app_commands.command(
        name='play',
        description='MUSICA TITO!!!'
    )
    async def play(self, interaction: discord.Interaction, url :str = None):
        voice_channel= interaction.user.voice.channel
        if voice_channel is None:
            embed = discord.Embed(title="{} entra al vc primero, BREA".format(interaction.user.name), color= discord.Color.red())
            await interaction.response.send_message(embed=embed)
        elif self.is_paused:
            self.vc.resume()
            self.is_paused = False
        else:
            song = self.get_yt_video_info(url)
            if type(song) == type(True):
                embed = discord.Embed(title="No se encontro el video", color=discord.Color.red())
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title='Se agrego a la cola:', description=song['title'], color=discord.Color.blue())
                embed.set_thumbnail(url=song['thumbnail'])
                await interaction.response.send_message(embed=embed)
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(interaction)
    
    @app_commands.command(
        name='pause',
        description='PAUSA TITO!!!!'
    )
    async def pause(self, interaction: discord.Interaction):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            embed = discord.Embed(title="Musica pausada", color= discord.Color.yellow())
            await interaction.response.send_message(embed=embed)
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @app_commands.command(
            name='resume',
            description='Que vuelva la musica'
    )
    async def resume(self, interaction: discord.Interaction):
        if self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            embed = discord.Embed(title="Musica reanudada", color= discord.Color.green())
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(
        name='skip',
        description="Salta un temazo"
    )
    async def skip(self, interaction: discord.Interaction):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
            await self.play_music(interaction)
            embed = discord.Embed(title="Se salto un temazo", color=discord.Color.yellow())
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(
        name='queue',
        description='Muestra lode temazos en cola'
    )
    async def queue(self, interaction: discord.Interaction):
        retval = ''
        for i in range(0, len(self.music_queue)):
            if i>5: break
            retval += self.music_queue[i][0]['title'] + '\n'
        
        if retval != '':
            embed = discord.Embed(title="Temazos en la cola:", description=retval, color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Sin temazos en la cola...", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name='clear',
        description=' Limpia la cola de temazos y detiene la musica'
    )
    async def clear(self, interaction: discord.Interaction):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue=[]
        embed = discord.Embed(title="Se limpio la cola y se detuvo la fiesta", color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(
        name='leave',
        description='Chao noma, TukiBot'
    )
    async def leave(self, interaction: discord.Interaction):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        embed = discord.Embed(title="Echaron a TukiBot, son fomes cabros... ", color= discord.Color.red())
        await interaction.response.send_message(embed=embed)

async def setup(TukiBot: commands.Bot) -> None:
    await TukiBot.add_cog(tusic(TukiBot))
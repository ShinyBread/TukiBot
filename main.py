import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from itertools import cycle
from pathlib import Path

load_dotenv("Token.env")  
TOKEN = os.getenv('TOKEN')

status = cycle(["Tuki", "tuki"])

class ShinyBotTest(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            application_id=1115333103213355030
        )
        self.initial_extensions = []

    async def setup_extensions(self):
        cogs_path = Path("cogs")
        for path in cogs_path.glob("**/*.py"):
            if path.is_file():
                cog = f"cogs.{path.parent.name}.{path.stem}"
                self.initial_extensions.append(cog)
                await self.load_extension(cog)
                print(f"Loaded cog: {cog}")

        await self.tree.sync()

    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(status)))

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f'{self.user} está listo!')
        await self.setup_extensions()

ShinyBot = ShinyBotTest()
ShinyBot.run(TOKEN)

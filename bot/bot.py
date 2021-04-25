import os
from pathlib import Path

import discord
from discord.ext  import commands
from dotenv import load_dotenv

load_dotenv()

class BumbleBeeBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True, intents=discord.Intents.all())
    
    def setup(self):
        print ("running setup")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"loaded cog: {cog}")
        
        print("Setup complete")
    
    def run(self):
        self.setup()
        TOKEN = os.getenv('DISCORD_TOKEN')
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("closing connection to Discord")
        await super().close()

    async def close(self):
        print("closing on keyboard interupt")
        await self.shutdown()
    
    async def on_connect(self):
        print(f"Conneced to Discord (latency: {self.latency*1000:,.0f} ms)")
    
    async def on_resumed(self):
        print("bot resumed")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready")
    
    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("!")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        if ctx.command is not None:
            await self.invoke(ctx)
    
    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
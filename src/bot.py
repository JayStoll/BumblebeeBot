import os
from pathlib import Path

import discord
from discord.ext  import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=discord.Intents().all())

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in')
    bot.load_extension('cogs.audio')

bot.run(os.getenv('DISCORD_TOKEN'))
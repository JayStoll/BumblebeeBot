import os

import discord
from discord.ext  import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def tell_me_about_yourself(ctx):
    text = "My name is BumbleBee!\n I was built by Jayden and Sam. At present I have limited features(find out more by typing !help)\n :)"
    await ctx.send(text)

if __name__ == "__main__":
    bot.run(TOKEN)
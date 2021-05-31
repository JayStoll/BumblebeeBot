from discord.ext import commands
from discord import utils
from discord import Embed
import discord
import lavalink
import re
import os
from dotenv import load_dotenv

load_dotenv()

url_rx = re.compile(r'https?://(?:www\.)?.+')

class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # create the lavalink server connection
        self.bot.audio = lavalink.Client(self.bot.user.id)
        self.bot.audio.add_node(
                os.getenv('LAVALINK_HOST'), 
                os.getenv('LAVALINK_PORT'), 
                os.getenv('LAVALINK_PASSWORD'), 
                os.getenv('LAVALINK_REGION'))
        self.bot.add_listener(self.bot.audio.voice_update_handler, 'on_socket_response')
        self.bot.audio.add_event_hook(self.track_hook)
    
    # dissconnect if no tracks left in queue - we may not want this but can be decided later
    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)
    
    # logic to connect to the voice channel
    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    ####################################################
    #
    # Bot Commands and error handeling 

    # Format of writting commands
    # @commands.command -> tells us that this is a command
    # @commandName_command.error -> error handeling 
    # name=... -> the name of the command we will use to signal the bot
    # help=... -> write a more detailed help description
    # aliases=[...] -> a different name given to the command

    @commands.command(name='join')
    async def join(self, ctx):
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.audio.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))
            else:
                await ctx.send("Already part of a channel")

    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        await self.connect_to(ctx.guild.id, None)

    # This is usefull not though we may remove this feature as it is not part of the scope of the project
    # It is here more for temporary test of the bot being able to play audio and how we can set up search queries   
    @commands.command(name="play", aliases=['p'])
    async def play(self, ctx, *, query):
        # Get the player for this guild from cache.
        player = self.bot.audio.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # we will have to do different checks later to use different websites
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = Embed(color=discord.Color.blurple())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()
    
    @commands.command(name="stop")
    async def stop(self, ctx):
        player = self.bot.audio.player_manager.get(ctx.guild.id)
        await player.stop()
    
def setup(bot):
    bot.add_cog(AudioCog(bot))
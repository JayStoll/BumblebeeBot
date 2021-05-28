from discord.ext import commands
from discord import utils
import lavalink

class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.audio = lavalink.Client(self.bot.user.id)
        self.bot.audio.add_node('localhost', 2333, 'youshallnotpass', 'na', 'Audio Node')
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

    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        await self.connect_to(ctx.guild.id, None)
    
    @commands.command(name='play')
    async def play(self, ctx, *, query):
        try:
            player = self.bot.audio.player_manager.get(ctx.guild.id)
            query = f'ytsearch:{query}' # this is for a youtube search, we will have to change this to use other things than youtube
            results = await player.node.get_tracks(query)
        except Exception as error:
            print(error)
    
def setup(bot):
    bot.add_cog(AudioCog(bot))
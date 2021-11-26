import discord
from discord.ext import commands, tasks
import youtube_dl


from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix=';')

token = "#"

status = ['Pop Music', 'Botflix', 'Bot Theft Auto 6', 'Botney Spears']


@client.event
async def on_ready():
    change_status.start()
    print("Bot is online!")



@client.command(name='hello', help=': Returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning', 'I couldve done so much more', 'I was having a great day until now']
    await ctx.send(choice(responses))

@client.command(name='play', help='This command plays music.')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to a voice channel')
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('player error: %s' %e) if e else None)

    await ctx.send(f'**Now playing:** {player.title}')


@client.command(name='stop', help='This command stops the song.')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run(token)



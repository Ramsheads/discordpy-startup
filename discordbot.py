import discord
from discord.ext import commands
import os
import traceback
import textwrap as tw

COMMAND_PREFIX="$$"
TOKEN_ENVIRON="DISCORD_BOT_TOKEN"
PON_WAV="ponn.wav"
token = os.environ[TOKEN_ENVIRON]
with open(PON_WAV, "r") as f:
    SOURCE=discord.PCMAudio(f)

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

# Yet implemented event handler
# on_member_join(member): ポンにゃテロ
# discord.on_voice_state_update(member, before, after):　来たにゃ！

def is_voice_connected():
    if bot.voice_clients:
        return True
    return False

@bot.event
async def on_ready():
    print("Start Ponnya Chan...")

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if "ポン" in ctx.content:
        await ctx.channel.send('ポンにゃ！')
        # if voice client already connected, say ポンにゃ！
        if is_voice_connected():
            for voice_client in bot.voice_clients:
                voice_client.play(SOURCE, after=lambda: print("Done"))
    
    try:
        await bot.process_commands(ctx)
    except Exception as e:
        await ctx.channel.send(
                "Ponnya Chan raised Exception:\n\t{}".format(e))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def connect(ctx):
    # VoiceClient connect
    author = ctx.message.author
    await ctx.channel.send("author: {}\n{}".format(author, dir(author)))
    await ctx.channel.send("voice:\n{}\nchannel:\n{}".format(
        dir(author.voice), dir(author.voice.channel)))
    await ctx.channel.send("bot:\n{}".format(dir(bot)))
    try:
        channel = author.voice.channel
    except:
        channel = None
    if channel != None:
        voice_client = await channel.connect()
        bot.voice_clients.append(voice_client)
    else:
        await ctx.channel.send(tw.dedent("""
        どのVoiceチャンネルに行けばいいかわからないにゃ！
        Voiceチャンネルに参加してからもう一度呼んでほしいにゃ！
        """))
        
@bot.command()
async def disconnect(ctx):
    #VoiceClient disconnect
    for voice_client in bot.voice_clients:
        await voice_client.disconnect()

@bot.command()
async def debug_info(ctx):
    await ctx.send(tw.dedent("""
    voice_clients: {vc}
    """.format(
        vc=bot.voice_clients,
    )))

bot.run(token)

import discord
from discord.ext import commands
import os
import traceback
import textwrap as tw

COMMAND_PREFIX="$$"
TOKEN_ENVIRON="DISCORD_BOT_TOKEN"
token = os.environ[TOKEN_ENVIRON]
PON_WAV="ponn.wav"
PON_WAV_FILE = open(PON_WAV, "rb")
PON_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(PON_WAV_FILE), volume=0.25)
JOIN_WAV="join.wav"
JOIN_WAV_FILE = open(JOIN_WAV, "rb")
JOIN_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(JOIN_WAV_FILE), volume=0.25)
RON_WAV="ron.wav"
RON_WAV_FILE = open(RON_WAV, "rb")
RON_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(RON_WAV_FILE), volume=0.25)
KAN_WAV="kan.wav"
KAN_WAV_FILE = open(KAN_WAV, "rb")
KAN_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(KAN_WAV_FILE), volume=0.25)
CHEE_WAV="chee.wav"
CHEE_WAV_FILE = open(CHEE_WAV, "rb")
CHEE_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(CHEE_WAV_FILE), volume=0.25)
PEI_WAV="pei.wav"
PEI_WAV_FILE = open(PEI_WAV, "rb")
PEI_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(PEI_WAV_FILE), volume=0.25)
REACH_WAV="reach.wav"
REACH_WAV_FILE = open(REACH_WAV, "rb")
REACH_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(REACH_WAV_FILE), volume=0.25)
TUMO_WAV="tumo.wav"
TUMO_WAV_FILE = open(TUMO_WAV, "rb")
TUMO_SOURCE=discord.PCMVolumeTransformer(
        discord.PCMAudio(TUMO_WAV_FILE), volume=0.25)

IS_DEBUG=False

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

def __play(voice_clinet, source, wav, msg):
    if voice_client.is_playing():
        voice_clinet.stop()
    source.cleanup()
    wav.seek(0)
    voice_client.play(source,
            after=lambda e: print("ERROR {}: {}".format(msg, e)))

def play(source, wav, msg):
    if is_voice_connected():
        for voice_client in bot.voice_clients:
            __play(voice_client, source, wav, msg)

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if "ポン" in ctx.content:
        await ctx.channel.send('ポンにゃ！')
        play(PON_SOURCE, PON_WAV_FILE, "on_message")

    if "ロン" in ctx.content:
        await ctx.channel.send('ロンにゃ！')
        play(RON_SOURCE, RON_WAV_FILE, "on_message")

    if "カン" in ctx.content:
        await ctx.channel.send('カンにゃ！')
        play(KAN_SOURCE, KAN_WAV_FILE, "on_message")

    if "チー" in ctx.content:
        await ctx.channel.send('チーにゃ！')
        play(CHEE_SOURCE, CHEE_WAV_FILE, "on_message")

    if "北" in ctx.content:
        await ctx.channel.send('ぺーにゃ！')
        play(PEI_SOURCE, PEI_WAV_FILE, "on_message")

    if "リーチ" in ctx.content:
        await ctx.channel.send('リーチにゃ！')
        play(REACH_SOURCE, REACH_WAV_FILE, "on_message")

    if "ツモ" in ctx.content:
        await ctx.channel.send('ツモにゃ！')
        play(TUMO_SOURCE, TUMO_WAV_FILE, "on_message")

    try:
        await bot.process_commands(ctx)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        await ctx.channel.send(
                "Ponnya Chan raised Exception:\n\t{}".format(e))

@bot.event
async def on_member_join(member):
    play(JOIN_SOURCE, JOIN_WAV_FILE, "on_member_join")

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
    try:
        channel = author.voice.channel
    except:
        channel = None
    if channel != None:
        try:
            if is_voice_connected():
                for vc in bot.voice_clients:
                    vc.move_to(channel)
            else:
                voice_client = await channel.connect()
                bot.voice_clients.append(voice_client)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print("ERROR on connect: {}".format(e))
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
    if not IS_DEBUG:
        return
    await ctx.send(tw.dedent("""
    voice_clients: {vc}
    source: {src} {src_dir}
    """.format(
        vc=bot.voice_clients,
        src=SOURCE, src_dir=dir(SOURCE)
    )))

bot.run(token)

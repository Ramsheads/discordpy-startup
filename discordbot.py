import discord
from discord.ext import commands
import os
import traceback
import textwrap as tw

COMMAND_PREFIX="$$"
TOKEN_ENVIRON="DISCORD_BOT_TOKEN"
PON_WAV="ponn.wav"
token = os.environ[TOKEN_ENVIRON]
PON_WAV_FILE = open(PON_WAV, "rb")
SOURCE=discord.PCMVolumeTransformer(discord.PCMAudio(PON_WAV_FILE))
IS_DEBUG=True

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
                try:
                    voice_client.play(SOURCE,
                            after=lambda e: print("ERROR on message: {}".format(e)))
                    SOURCE.cleanup()
                    PON_WAV_FILE.seek(0)
                except Exception as e:
                    await ctx.channel.send("ERROR on message: {}".format(e))
    
    try:
        await bot.process_commands(ctx)
    except KeyboardInterrupt:
        exit()
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

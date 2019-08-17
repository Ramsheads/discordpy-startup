import discord
from discord.ext import commands
import os
import traceback
import textwrap as tw
import re

COMMAND_PREFIX="$$"
TOKEN_ENVIRON="DISCORD_BOT_TOKEN"
token = os.environ[TOKEN_ENVIRON]
#TODO: Need to make them class

class VoiceSource:
    def __init__(self, bot, path, default_vol=0.25, pattern="", msg=""):
        self.bot=bot

        if not isinstance(path, str):
            raise TypeError("path should be str")
        self.path=path

        if not isinstance(default_vol, (int, float)):
            raise TypeError("default_vol should be int or float")
        if default_vol < 0 or default_vol > 1:
            raise ValueError("default_vol should be 0.0 ~ 1.0")
        self.default_vol=default_vol

        if not isinstance(pattern, str):
            raise TypeError("pattern should be str")
        self.pattern=pattern
    
        if not isinstance(msg, str):
            raise TypeError("msg should be str")
        self.msg=msg

        self.__set_src__()
        self.__set_regex__()
    
    def __set_src__(self):
        self._file=open(self.path, "rb")
        self._src=discord.PCMVolumeTransformer(
            discord.PCMAudio(self._file),
            volume=self.default_vol
        )
    
    def __set_regex__(self):
        self._regex=re.compile(self.pattern)

    #FIXME: Need to use on multiple servers
    def play(self):
        for vc in self.bot.voice_clients:
            if vc.is_playing():
                vc.stop()
            self._src.cleanup()
            self._file.seek(0)
            vc.play(
                self._src,
                after=lambda e: print(
                    "ERROR {}: {}".format(self.path, e)))
    
    def say(self, ctx):
        if self.msg:
            await ctx.channel.send(self.msg)
    
    def check_play(self, ctx):
        if re.search(self._regex, ctx.content):
            try:
                self.say(ctx)
                self.play()
            except Exception as e:
                await ctx.channel.send(
                    "ERROR on {}: {}".format(ctx.content, e))
            return True
        return False

IS_DEBUG=False

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

vs_pon = VoiceSource(bot,
    "ponn.wav", pattern=r'ポン|ぽん', msg='ポンにゃ！')
vs_ron = VoiceSource(bot,
    "ron.wav", pattern=r'ロン|ろん', msg='ロンにゃ！')
vs_kan = VoiceSource(bot,
    "kan.wav", pattern=r'カン|かん', msg='カンにゃ！')
vs_sukan = VoiceSource(bot,
    "sukan.wav", pattern=r'カン|かん', msg='スーカンながれにゃー……')
SUKAN_COUNT=0
vs_chee = VoiceSource(bot,
    "chee.wav", pattern=r'チー|ちー', msg='チーにゃ！')
vs_pei = VoiceSource(bot,
    "pei.wav", pattern=r'北|ペー|ぺー', msg='ペーにゃ！')
vs_suhu = VoiceSource(bot,
    "suhu.wav", pattern=r'北|ペー|ぺー', msg='スーフーにゃんだにゃー……')
SUHU_COUNT=0
vs_reach = VoiceSource(bot,
    "reach.wav", pattern=r'リーチ|りーち', msg='リーチにゃ！')
vs_tumo = VoiceSource(bot,
    "tumo.wav", pattern=r'ツモ|つも', msg='ツモにゃ！')

# Yet implemented event handler
# on_member_join(member): ポンにゃテロ
# discord.on_voice_state_update(member, before, after):　来たにゃ！

@bot.event
async def on_ready():
    print("Start Ponnya Chan...")

def clear_sukan():
    global SUKAN_COUNT
    SUKAN_COUNT = 0

def is_sukan():
    global SUKAN_COUNT
    SUKAN_COUNT += 1
    if SUKAN_COUNT != 0 and SUKAN_COUNT % 4 == 0:
        clear_sukan()
        return True
    return False

def clear_suhu():
    global SUHU_COUNT
    SUHU_COUNT = 0

def is_suhu():
    global SUHU_COUNT
    SUHU_COUNT += 1
    if SUHU_COUNT != 0 and SUHU_COUNT % 4 == 0:
        clear_suhu()
        return True
    return False

def clear_all_counter():
    clear_suhu()
    clear_sukan()

@bot.event
async def on_message(ctx):
    global SUKAN_COUNT
    if ctx.author == bot.user:
        return
    
    try:
        if vs_pon.check_play(ctx):
            pass
        elif vs_chee.check_play(ctx):
            pass
        elif vs_ron.check_play(ctx):
            clear_all_counter()
        elif vs_tumo.check_play(ctx):
            clear_all_counter()
        elif vs_reach.check_play(ctx):
            pass
        elif vs_kan.check_play(ctx):
            if is_sukan():
                vs_sukan.say(ctx)
                vs_sukan.play()
                clear_all_counter()
        elif vs_pei.check_play(ctx):
            if is_suhu():
                vs_suhu.say(ctx)
                vs_suhu.play()
                clear_all_counter()
        else:
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
    # Try to connect a voice channel that author joined
    author = ctx.message.author
    try:
        channel = author.voice.channel
    except:
        channel = None
    #FIXME: Need to connect multiple voice channels over the servers
    if channel != None:
        try:
            if bot.voice_clients:
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
    #FIXME: Need to disconnect a single channel based on ctx
    #VoiceClient disconnect
    for voice_client in bot.voice_clients:
        await voice_client.disconnect()

@bot.command()
async def debug_info(ctx):
    if not IS_DEBUG:
        return
    await ctx.send(tw.dedent("""
    voice_clients: {vc}
    sukan: {sukan}
    suhu: {suhu}
    """.format(
        vc=bot.voice_clients,
        sukan=SUKAN_COUNT,
        suhu=SUHU_COUNT,
    )))

bot.run(token)

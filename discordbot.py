#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import discord
from discord.ext import commands
import os
import traceback
import textwrap as tw
import re
import time
import jaconv
from voice_source import VoiceSource, raw_or

# bot
COMMAND_PREFIX="$$"
TOKEN_ENVIRON="DISCORD_BOT_TOKEN"
token = os.environ[TOKEN_ENVIRON]

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

# util
hira2hirakata=lambda s: [s, jaconv.hira2kata(s)]
IS_DEBUG=False

# keyword for actions
keyword_pon=hira2hirakata('ぽん')
keyword_ron=hira2hirakata('ろん')
keyword_kan=hira2hirakata('かん')
keyword_chee=hira2hirakata('ちー')
keyword_pei=hira2hirakata('ぺー')
keyword_pei.append('北')
keyword_reach=hira2hirakata('りーち')
keyword_tumo=hira2hirakata('つも')

keywords = (
    keyword_pon,
    keyword_ron,
    keyword_kan,
    keyword_chee,
    keyword_pei,
    keyword_reach,
    keyword_tumo,
)

if IS_DEBUG:
    for i in keywords:
        print("{} -> {}".format(i, raw_or(i)))

# variables for actions

SUKAN_COUNT=0
SUHU_COUNT=0

# voice sources
vs_pon = VoiceSource(bot,
    "ponn.wav", pattern=raw_or(keyword_pon), msg='ポンにゃ！')
vs_ron = VoiceSource(bot,
    "ron.wav", pattern=raw_or(keyword_ron), msg='ロンにゃ！')
vs_kan = VoiceSource(bot,
    "kan.wav", pattern=raw_or(keyword_kan), msg='カンにゃ！')
vs_sukan = VoiceSource(bot,
    "sukan.wav", pattern=raw_or(keyword_kan), msg='スーカンながれにゃー……')
vs_chee = VoiceSource(bot,
    "chee.wav", pattern=raw_or(keyword_chee), msg='チーにゃ！')
vs_pei = VoiceSource(bot,
    "pei.wav", pattern=raw_or(keyword_pei), msg='ペーにゃ！')
vs_suhu = VoiceSource(bot,
    "suhu.wav", pattern=raw_or(keyword_pei), msg='スーフーにゃんだにゃー……')
vs_reach = VoiceSource(bot,
    "reach.wav", pattern=raw_or(keyword_reach), msg='リーチにゃ！')
vs_tumo = VoiceSource(bot,
    "tumo.wav", pattern=raw_or(keyword_tumo), msg='ツモにゃ！')

print("create bot and voice sources")

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
    if ctx.author == bot.user:
        return
    
    if vs_pon.check_play(ctx):
        await ctx.channel.send(vs_pon.msg)
    elif vs_chee.check_play(ctx):
        await ctx.channel.send(vs_chee.msg)
    elif vs_ron.check_play(ctx):
        await ctx.channel.send(vs_ron.msg)
        clear_all_counter()
    elif vs_tumo.check_play(ctx):
        await ctx.channel.send(vs_tumo.msg)
        clear_all_counter()
    elif vs_reach.check_play(ctx):
        await ctx.channel.send(vs_reach.msg)
    elif vs_kan.check_play(ctx):
        await ctx.channel.send(vs_kan.msg)
        if is_sukan():
            time.sleep(0.5)
            await ctx.channel.send(vs_sukan.msg)
            vs_sukan.play()
            clear_all_counter()
    elif vs_pei.check_play(ctx):
        await ctx.channel.send(vs_pei.msg)
        if is_suhu():
            time.sleep(0.5)
            await ctx.channel.send(vs_suhu.msg)
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
print("bot running")

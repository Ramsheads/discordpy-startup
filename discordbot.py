from discord.ext import commands
import os
import traceback
import textwrap as tw

COMMAND_PREFIX="/"
TOKEN_ENVIRON="DISCORD_BOT_TOKEN"
bot = commands.Bot(command_prefix=COMMAND_PREFIX)
token = os.environ[TOKEN_ENVIRON]
# VoiceClientつくって bot.voice_clients に入れる？

@bot.event
async def on_ready():
    print("Start Ponnya Chan...")

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if "ポン" in ctx.content:
        await ctx.channel.send('ポンにゃ！')
    
    try:
        await bot.process_commands(ctx)
    except Exception:
        await ctx.channel.send(f'```\n{traceback.format_exc()}\n```')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def debug_info(ctx):
    await ctx.send(tw.dedent("""
    voice_clients: {vc}
    """.format(
        vc=bot.voice_clients
    ))

bot.run(token)

import discord
from discord.ext import commands, tasks
import Leetcode as lc

TOKEN = open('TOKEN.txt', 'r').readline()

bot = commands.Bot(command_prefix='!')

leetcodeIDList = {'quangvn2508':0, 'nnv': 0}

@bot.event
async def on_ready():
    stalk.start()
    print('Bot is ready')

@bot.command()
async def ping(ctx):
    await ctx.send(f'{ctx.author}\'s ping is {round(bot.latency * 1000)}ms')

@bot.command()
async def add(ctx, username):
    p, c = lc.mostRecentSubmission(str(username))
    print(username, p, c)
    if p == None:
        await ctx.send(f'Bot could not find leedcode with id **{username}**')
    else:
        leetcodeIDList[username] = c
        await ctx.send(f'leedcode ID **{username}** is added')

@tasks.loop(seconds=10)
async def stalk():
    channel = bot.get_channel(754253458630246493)
    for lcid, lcc in leetcodeIDList.items():
        p, c = lc.mostRecentSubmission(lcid)
        if p == None:
            continue
        if c > lcc:
            await channel.send(f'**{lcid}** just solved question **{p}**')
            leetcodeIDList[lcid] = c



bot.run(TOKEN)
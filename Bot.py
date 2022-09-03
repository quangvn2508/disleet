import discord
from discord.ext import tasks
from Leetcode import get_total_question_solved, get_recent_AC_submission
from utils import log, timestampToString
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
NOTIFICATION_CHANNEL = int(os.getenv('NOTIFICATION_CHANNEL'))
bot = discord.Bot()

leetcodeUsersList = {}

@bot.event
async def on_ready():
    stalk.start()
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "ping", description = "Get user's latency to bot server")
async def ping(ctx):
    await ctx.respond(f'{ctx.author}\'s ping is {round(bot.latency * 1000)}ms')

@bot.slash_command(name = "add_leetcode", description = "Add a leetcode profile to be tracked")
async def add(ctx, username):
    if username in leetcodeUsersList:
        await ctx.respond(f"User **{username}** already been tracked")
        return

    count, error = get_total_question_solved(username)
    if error != None:
        await ctx.respond(f"Unable to get status for **{username}** with error [{error}]")
    else:
        leetcodeUsersList[username] = count
        await ctx.respond(f'User\'s added, **{username}** solved {count} questions')

@tasks.loop(seconds=5)
async def stalk():
    channel = bot.get_channel(NOTIFICATION_CHANNEL)
    for username, question_count in leetcodeUsersList.items():
        count, error = get_total_question_solved(username)
        print(count)
        if error != None:
            log(f"error [{error}] when stalking user {username}")
            continue
        if count < question_count:
            log(f"something wrong, current solved questions ({count}) smaller than server recorded ({question_count}) for user {username}")
            continue
        if count == question_count:
            continue
        leetcodeUsersList[username] = count

        new_quesiton, error =  get_recent_AC_submission(username)
        if error != None:
            log(f"error [{error}] when get recent AC for user {username}")
            continue
        await channel.send(f"**{username}** just solved **{new_quesiton['title']}** (https://leetcode.com/problems/{new_quesiton['titleSlug']}/) at {timestampToString(new_quesiton['timestamp'])}")

bot.run(TOKEN)
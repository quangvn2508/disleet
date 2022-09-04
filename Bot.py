import discord
from discord.ext import tasks
from Leetcode import get_total_question_solved, get_recent_AC_submission
from utils import log, timestampToString, loadUsers, saveUser
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
NOTIFICATION_CHANNEL = int(os.getenv('NOTIFICATION_CHANNEL'))
bot = discord.Bot()

usernameAndQuestionCount = {}
usernameList = []
nextUser = 0
userCount = 0

@bot.event
async def on_ready():
    stalk.start()
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "ping", description = "Get user's latency to bot server")
async def ping(ctx):
    await ctx.respond(f'{ctx.author}\'s ping is {round(bot.latency * 1000)}ms')

@bot.slash_command(name = "add_leetcode", description = "Add a leetcode profile to be tracked")
async def add(ctx, username):
    if username in usernameAndQuestionCount:
        await ctx.respond(f"User **{username}** already been tracked")
        return

    global userCount
    count, error = get_total_question_solved(username)
    if error != None:
        await ctx.respond(f"Unable to get status for **{username}** with error [{error}]")
    else:
        usernameAndQuestionCount[username] = count
        usernameList.append(username)
        userCount = len(usernameList)
        saveUser(username)
        await ctx.respond(f'User\'s added, **{username}** solved {count} questions')

@tasks.loop(seconds=1)
async def stalk():
    channel = bot.get_channel(NOTIFICATION_CHANNEL)
    if userCount == 0:
        return
    global nextUser
    username = usernameList[nextUser]
    nextUser = (nextUser + 1) % userCount
    question_count = usernameAndQuestionCount[username]

    count, error = get_total_question_solved(username)
    if error != None:
        log(f"error [{error}] when stalking user {username}")
        return
    if count == question_count:
        return

    usernameAndQuestionCount[username] = count
    if count < question_count:
        log(f"something wrong, current solved questions ({count}) smaller than server recorded ({question_count}) for user {username}")
        return
    new_quesiton, error =  get_recent_AC_submission(username)
    if error != None:
        log(f"error [{error}] when get recent AC for user {username}")
        return
    await channel.send(f"**{username}** just solved **{new_quesiton['title']}** (https://leetcode.com/problems/{new_quesiton['titleSlug']}/) at {timestampToString(new_quesiton['timestamp'])}")

if __name__ == "__main__":
    usernameList = loadUsers()
    for username in usernameList:
        count, error = get_total_question_solved(username)
        if error != None:
            log(f"error [{error}] when get recent AC for user {username}")
            continue
        usernameAndQuestionCount[username] = count
    userCount = len(usernameList)
    bot.run(TOKEN)
import os
import discord
import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
from dataclasses import dataclass

load_dotenv()

print("getting credentials from .env")
TOKEN = os.getenv('AUTH_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
MAX_SESSION_TIME_MINUTES = 2 # following this tutorial https://www.youtube.com/watch?v=2k9x0s3awss

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

session = Session()

@bot.event
async def on_ready():
    print('Hello! Study bot is ready')
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send("Hello bot is ready!")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():

    if break_reminder.current_loop == 0: # ignore init task
        return

    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send(f"You have been studying for a while, you **should take a break**. It's been **{MAX_SESSION_TIME_MINUTES} minutes!**") # **bold**

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")
"""
@bot.command()
async def add(ctx, x, y): #this version will ignore subsequent values
    z = int(x) + int(y)
    await ctx.send(f"{x} + {y} = {z}")  
"""

@bot.command()
async def add(ctx, *arr):
    z = 0

    for i in arr:
        z+= int(i)

    await ctx.send(f"Result = {z}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    break_reminder.start()
    session.start_time = ctx.message.created_at.timestamp()
    time_stamp= ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"New study session started at {time_stamp}")

@bot.command()
async def end(ctx):
    if session.is_active:
        break_reminder.stop()
        end_time = ctx.message.created_at.timestamp()
        session.is_active = False
        duration = str(datetime.timedelta(seconds=end_time - session.start_time))
        time_stamp= ctx.message.created_at.strftime("%H:%M:%S")
        await ctx.send(f"Study session ended at {time_stamp} with a duration of {duration} seconds")
        return

    await ctx.send(f"No running session start a new session")

bot.run(TOKEN)
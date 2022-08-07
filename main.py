
import discord
import os
import asyncio
from discord.ext import tasks

from datetime import datetime, timedelta
from pytz import timezone
from birthdays import dateToPerson, birthdayMsgs
from greetings import greetings

from stay_awake import stay_awake
import random
import operator

# this keeps the bot running even when the repo's not open
stay_awake()

token = os.environ['TOKEN']

facts = open("facts.txt", "r").readlines()

bot = discord.Client()

intents = discord.Intents.none()
intents.reactions = True
intents.members = True
intents.guilds = True

@bot.event
async def on_ready():
  print("Logged in as {0.user}".format(bot))

################## BIRTHDAYS ##################

eastern = timezone('US/Eastern')
  
def seconds_until_midnight():
    now = datetime.now().astimezone(eastern)
    target = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    diff = (target - now).total_seconds()
    print(f"{target} - {now} = {diff}")
    return diff

def getBirthdayBoi():
  now = datetime.now().astimezone(eastern)
  
  for date, person in dateToPerson.items():
    if now.month == date.month and now.day == date.day:
      print(f"Happy birthday {person}")
      age = now.year() - date.year()
      return [person, age]
    
  return ""

@tasks.loop(seconds=1)
async def called_once_a_day_at_midnight():
    await asyncio.sleep(seconds_until_midnight())
    print("Midnight!")
  
    message_channel = bot.get_channel(820122151696597055) # in texting-taters
    print(f"Got channel {message_channel}")
  
    birthdayBoi = getBirthdayBoi()
  
    if birthdayBoi != "":
      await message_channel.send("@everyone " + birthdayMsgs[birthdayBoi[0]] + " " + birthdayBoi + " just turned " + str(birthdayBoi[1]) + ", give them a pat 🥳")
      # await message_channel.send(asciiArt[birthdayBoi])

@called_once_a_day_at_midnight.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

################## GENERAL ##################
  
@bot.event
async def on_message(message):
  if message.author == bot:
    return
  
  # basic greeting
  if message.content.startswith("#hello"):
    await message.channel.send(random.choice(greetings))

  # echo your message
  if message.content.startswith("#echo"):
    await message.channel.send(message.content[5:].strip())
  
  # greeting with mention
  if "#hi taterbot" in message.content:
    await message.channel.send(random.choice(greetings)[:-1] + ", <@" + str(message.author.id) + ">!")

    # mention you and everyone else you tag
    for mention in message.mentions:
      await message.channel.send(random.choice(greetings)[:-1] + ", <@" + str(mention.id) + ">!")

  # create a text channel (same category as the channel you're currently in)
  if message.content.startswith("#channel"):
    channel_name = message.content[8:].strip()
    await message.channel.category.create_text_channel(channel_name)

  # perform a simple one-step calculation
  if message.content.startswith("#math"):
    calculate = message.content[5:].strip()

    operators = ['+','-','*','/','^']
    ops = {"+": operator.add, "-": operator.sub, "*":operator.mul, "/":operator.truediv, "^":operator.pow}

    operator_char = ''
    
    for char in calculate:
      if char in operators:
        operator_char = char
        result = ops[operator_char](float(calculate[:calculate.index(char)]),float(calculate[calculate.index(char)+1:]))
        break
    await message.channel.send(result)

  if "#fact" in message.content or "#are you smart" in message.content:
    await message.channel.send(random.choice(facts))

called_once_a_day_at_midnight.start()
bot.run(token)
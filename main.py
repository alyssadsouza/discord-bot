
import discord
import os
from stay_awake import stay_awake

import random
import operator

# this keeps the bot running even when the repo's not open
stay_awake()

token = os.environ['TOKEN']

greetings = ['Hello!', "Hi!", "Hey!", "Oh, I didn't see you there!", "Hello there!"]

bot = discord.Client()

@bot.event
async def on_ready():
  print("Logged in as {0.user}".format(bot))

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
  if message.content.startswith("#hi taterbot"):
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


bot.run(token)
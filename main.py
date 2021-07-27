import discord
from discord.ext import commands, tasks
import os
from binance.client import Client
from datetime import datetime
import time
from pytz import timezone
from keep_alive import keep_alive

# Binance API
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client_binance = Client(api_key, api_secret)

# Discord setup
intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(name='$', type=discord.ActivityType.listening)
client_discord = commands.Bot(command_prefix = '$', intents=intents, activity=activity)

def usage_msg(cmd, usage):
  return '**Usage**: {0} {1}'.format(cmd, usage)

@client_discord.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client_discord))

@client_discord.event
async def on_message(message):
  if message.author == client_discord.user:
    return

  msg = message.content.lower()

  # Getting crypto price from Binance
  if msg.startswith('$'):
    if msg.startswith('$price') or msg.startswith('$p'):
      if msg == '$price' or msg == '$p':
        await message.channel.send(usage_msg(msg, '[CRYPTO_CODE]\n*PHP to USD set at 50'))
      else:
        try:
          coin = ''.join(msg.split()[1:]).upper()
          query = client_binance.get_symbol_ticker(symbol=coin+"USDT")
        except:
          await message.channel.send('Invalid crypto code.')
        else:
          now = datetime.now(timezone("Asia/Hong_Kong"))
          dt_string = now.strftime("%m/%d/%Y **|** %I:%M %p")
          price_usd = float(query.get('price'))
          price_php = price_usd*50
          await message.channel.send("**{0}** Price: ${1} ≈ P{2}\n{3}".format(coin, str(price_usd), str(round(price_php,2)), dt_string))
    elif msg.startswith('$axie'):
      pass

  elif msg.startswith('i love you'):
    await message.channel.send("I love you too, {0.author.mention}!".format(message))

@client_discord.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
        f"Hi {member.name}, welcome to the Axie Scholarship Discord Server!\nHere's to our journey together, and we hope you enjoy earning from Axie Infinity!\n\nPlease don't hesitate to chat in our Discord Server if you have any questions!"
    )
  role = discord.utils.get(member.guild.roles, name='Scholar')
  await member.add_roles(role)

# @tasks.loop(seconds=5.0)
# async def send_message():
#   channel = client_discord.get_channel(869113270315929651)
#   print(channel)
#   await channel.send("Message")

keep_alive()
client_discord.run(os.environ['BOT_TOKEN'])
# send_message.start()

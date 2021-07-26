import discord
from discord.ext import commands
import os
from binance.client import Client
from datetime import datetime


api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client_binance = Client(api_key, api_secret)

intents = discord.Intents.default()
intents.members = True
client_discord = commands.Bot(command_prefix = '$', intents=intents)

@client_discord.event
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client_discord))

@client_discord.event
async def on_message(message):
  if message.author == client_discord.user:
    return

  msg = message.content

  if msg.startswith('$price'):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    coin = ''.join(msg.split()[1:]).upper()
    query = client_binance.get_symbol_ticker(symbol=coin+"USDT")
    price = str(float(query.get('price')))
    await message.channel.send("**{0}** Price: ${1} \nas of {2}"
    .format(coin, price, dt_string))

@client_discord.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
        f"Hi {member.name}, welcome to the Axie Scholarship Discord Server! Here's to our journey together, and we hope you enjoy earning from Axie Infinity!"
    )
  await member.dm_channel.send(
        f"Please don't hesitate to chat in our Discord Server if you have any questions!"
    )
  role = discord.utils.get(member.guild.roles, name='Scholar')
  await member.add_roles(role)


client_discord.run(os.environ['BOT_TOKEN'])


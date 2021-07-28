import discord
from discord.ext import commands
import os
from binance.client import Client
from datetime import datetime
from pytz import timezone
from keep_alive import keep_alive

# Binance API
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client_binance = Client(api_key, api_secret)

# Discord setup
intents = discord.Intents.all()
intents.members = True
activity = discord.Activity(name='$', type=discord.ActivityType.listening)
bot = commands.Bot(command_prefix = '$', intents=intents, activity=activity)

# Changed client_discord to bot #
#################################

def usage_msg(cmd, usage):
  return '**Usage**: {0} {1}'.format(cmd, usage)

def get_coin(code):
  query = client_binance.get_symbol_ticker(symbol=code.upper()+"USDT")
  return query

@bot.command(pass_context=True, aliases=['p'])
async def price(ctx, coin: str = None):
  # Getting crypto price from Binance then sending it to chat.
  if not coin:
    await ctx.send(usage_msg(ctx.message.content, '*[crypto_code]*\n*PHP to USD set at 50'))
  else:
    try:
      coin_pair = get_coin(coin)
    except:
      await ctx.send('Invalid crypto code.')
    else:
      now = datetime.now(timezone("Asia/Hong_Kong"))
      dt_string = now.strftime("%m/%d/%Y **|** %I:%M %p")

      price_usd = float(coin_pair.get('price'))
      price_php = price_usd*50
      await ctx.send("**{0}** Price: ${1} ≈ P{2}\n{3}".format(coin.upper(), str(price_usd), str(round(price_php,2)), dt_string))

@bot.command(pass_context=True, aliases=['calc', 'c'])
async def calculate(ctx, coin: str = None, usd_sellprice: float = None):
  # Calculating how much ETH to sell Axie for based on USD value
  if not coin or not usd_sellprice:
    await ctx.send(usage_msg(ctx.message.content, '*[crypto_code]* *[usd_sell_price]*'))
  else:
    try:
      coin_pair = get_coin(coin)
    except:
      await ctx.send('Invalid crypto code.')
    else:
      coin_price_usd = float(coin_pair.get('price'))
      result = usd_sellprice/coin_price_usd
      await ctx.send("${0} = {1} {2}".format(str(usd_sellprice), str(round(result, 4)), coin.upper()))


  # await message.channel.send(usage_msg(msg, '[CRYPTO_CODE]\n*PHP to USD set at 50'))


    


# @client_discord.event
# async def on_ready():
#   print('We have logged in as {0.user}'
#   .format(client_discord))

# @client_discord.event
# async def on_message(message):
#   if message.author == client_discord.user:
#     return

#   msg = message.content.lower()



#   elif msg.startswith('i love you'):
#     await message.channel.send("I love you too, {0.author.mention}!".format(message))

@bot.event
async def on_member_join(member):
  await member.send(
        f"Hi {member.name}, welcome to the Axie Scholarship Discord Server!\nHere's to our journey together, and we hope you enjoy earning from Axie Infinity!\n\nPlease don't hesitate to chat in *#scholars* if you have any questions!"
    )
  role = discord.utils.get(member.guild.roles, name='Scholar')
  await member.add_roles(role)

# @tasks.loop(seconds=5.0)
# async def send_message():
#   channel = client_discord.get_channel(869113270315929651)
#   print(channel)
#   await channel.send("Message")

keep_alive()
bot.run(os.environ['BOT_TOKEN'])

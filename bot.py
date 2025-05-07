import discord
from discord.ext import commands
import os 

from dotenv import load_dotenv
load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.invites = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.load_extension("cogs.komendy")
    await bot.load_extension("cogs.moderacja")
    await bot.load_extension("cogs.invites")
    await bot.load_extension("cogs.giveaway")
    
    
from dotenv import load_dotenv
load_dotenv()  

bot.run(os.getenv('DISCORD_TOKEN'))
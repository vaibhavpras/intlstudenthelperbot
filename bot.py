# bot.py
import os

import discord
from dotenv import load_dotenv

from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import nicknamecheck
import rolereaction

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.guilds}')

    
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    await nicknamecheck.nicknameCheck(message)    
    
    
bot.run(TOKEN)
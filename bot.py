# bot.py
import os

import discord
from dotenv import load_dotenv

from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions

import nicknamecheck
import rolereaction

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix='!')


@bot.command(name = "add_country", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_country(ctx, arg):
    with open('countries.txt', 'a') as f:
        f.write(f"""\n{arg}""")
    await ctx.channel.send(f"""Added {arg} to the list of countries""")

@add_country.error
async def add_country_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.guilds}')

    
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    await nicknamecheck.nicknameCheck(message)       
    
bot.run(TOKEN)
# bot.py
import os

import discord
from dotenv import load_dotenv

import datetime
from datetime import timedelta
from datetime import datetime

from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix='!')

alerted_list = {}

def checkKey(dict, key):       
    if key in dict.keys(): 
        return 1
    else: 
        return 0 

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.guilds}')


@bot.command()
async def add_country(ctx, arg):
    with open('countries.txt', 'a') as f:
        f.write(f"""\n{arg}""")
    await ctx.channel.send(f"""Added {arg} to the list of countries""")

@bot.event
async def on_message(message):

    if not message.author.nick:
        await message.channel.send(f"""{message.author.mention} please add a nickname which has your country and college name (if applicable).""")
        return

    with open('countries.txt', 'r') as f:
        countries_list = [line.strip() for line in f]


    countries_list = [item.lower() for item in countries_list]

    nickname  = (message.author.nick).lower()

    if (message.author.bot):
        return
    
    print(message.author.nick)            

    #isCountryAdded = [ele for ele in countries_list if(ele in nickname)] 
    isCountryAdded = any(ele in nickname for ele in countries_list) 

    isAlerted = checkKey(alerted_list, message.author.nick)

    #print(isAlerted)
    #print(nickname)
    print(isCountryAdded)

    if isAlerted == 1:
        date1 = alerted_list[message.author.nick]
        date2 = datetime.now()

        difference = (date2 - date1).total_seconds()
        
        #print (difference)

        inSeconds = difference
        if inSeconds > 120 and not isCountryAdded:
            await message.channel.send(f"""{message.author.mention} please add your country to your nickname""")
            alerted_list.update( {message.author.nick : datetime.now()} )
        elif inSeconds > 120 and isCountryAdded:
            del alerted_list[message.author.nick] 
            await bot.process_commands(message)
            return
        else:
            await bot.process_commands(message)
            return    

    else:
        if not isCountryAdded:
            await message.channel.send(f"""{message.author.mention} please add your country to your nickname""")
            alerted_list.update( {message.author.nick : datetime.now()} )
            #print (alerted_list)

    await bot.process_commands(message)
    
    
bot.run(TOKEN)
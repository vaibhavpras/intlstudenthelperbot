# bot.py
import os

import discord
from dotenv import load_dotenv

import datetime
from datetime import timedelta
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

with open('countries.txt', 'r') as f:
    countries_list = [line.strip() for line in f]


countries_list = [item.lower() for item in countries_list]

alerted_list = {}

def checkKey(dict, key):       
    if key in dict.keys(): 
        return 1
    else: 
        return 0 

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'{client.guilds}')

@client.event
async def on_message(message):

    if not message.author.nick:
        await message.channel.send(f"""{message.author.mention} please add a nickname which has your country and college name (if applicable).""")
        return

    nickname  = (message.author.nick).lower()

    if (message.author.bot):
         return

    
    print(message.author.nick)    
           

    #isCountryAdded = [ele for ele in countries_list if(ele in nickname)] 
    isCountryAdded = any(ele in nickname for ele in countries_list) 

    isAlerted = checkKey(alerted_list, message.author.nick)

    #print(isAlerted)
    #print(nickname)
    #print(isCountryAdded)

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
            return
        else:
            return    

    else:
        if not isCountryAdded:
            await message.channel.send(f"""{message.author.mention} please add your country to your nickname""")
            alerted_list.update( {message.author.nick : datetime.now()} )
            #print (alerted_list)
    
    
client.run(TOKEN)
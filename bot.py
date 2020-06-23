# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

with open('countries.txt', 'r') as f:
    countries_list = [line.strip() for line in f]


temp_list = ["India", "China", "Pakistan"]

countries_list = [item.lower() for item in countries_list]



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'{client.guilds}')

@client.event
async def on_message(message):
    nickname  = (message.author.nick).lower()

    if (message.author.bot):
         return

    #isCountryAdded = [ele for ele in countries_list if(ele in nickname)] 
    isCountryAdded = any(ele in nickname for ele in countries_list) 

    print(nickname)

    print(isCountryAdded)

    test = bool(isCountryAdded)

    if not test:
        await message.channel.send(f"""{message.author.mention} Please add your country to your nickname""")
    
client.run(TOKEN)
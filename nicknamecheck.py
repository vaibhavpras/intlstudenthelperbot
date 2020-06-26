import os

import discord

import datetime
from datetime import timedelta
from datetime import datetime

alerted_list = {}


def checkKey(dict, key):       
    if key in dict.keys(): 
        return 1
    else: 
        return 0 

async def nicknameCheck(message):
    if (message.author.bot):
        return        
  

    if message.author.nick: 

        nickname  = (message.author.nick).lower()   

        with open('countries.txt', 'r') as f:
            countries_list = [line.strip() for line in f]
            countries_list = [item.lower() for item in countries_list] 

        #isCountryAdded = [ele for ele in countries_list if(ele in nickname)] 
        isCountryAdded = any(ele in nickname for ele in countries_list)

        isAlerted = checkKey(alerted_list, message.author.nick)

        print(f""""{nickname}" isAlerted: {isAlerted} & isCountryAdded: {isCountryAdded}""")
    

        if isAlerted == 1:
            date1 = alerted_list[message.author.nick]
            date2 = datetime.now()

            difference = (date2 - date1).total_seconds()
        
            print (f""" Time since alerted: {difference}""")

            inSeconds = difference
            if inSeconds > 600 and not isCountryAdded:
                await message.channel.send(f"""{message.author.mention} please add your country to your nickname""")
                alerted_list.update( {message.author.nick : datetime.now()} )
            elif inSeconds > 600 and isCountryAdded:
                del alerted_list[message.author.nick] 
                return
            else:
                return 

        else:
            if not isCountryAdded:
                await message.channel.send(f"""{message.author.mention} please add your country to your nickname""")
                alerted_list.update( {message.author.nick : datetime.now()} )
                return

    else: 
        isAlertedNoNick = checkKey(alerted_list, message.author.name)
        print(f""""{message.author.name}" isAlerted: {isAlertedNoNick}""")
    

        if isAlertedNoNick == 1:
            date1 = alerted_list[message.author.name]
            date2 = datetime.now()

            difference = (date2 - date1).total_seconds()
        
            print (f"""Time since alerted: {difference}""")

            inSeconds = difference
            if inSeconds > 600 and not message.author.nick:
                await message.channel.send(f"""{message.author.mention} please add a nickname which has your country and college name (if applicable).""")
                alerted_list.update( {message.author.name : datetime.now()} )
            elif inSeconds > 600 and message.author.nick:
                del alerted_list[message.author.name]
                nicknameCheck(message)             
                return
            else:
                return    

        else:
            if not message.author.nick:
                await message.channel.send(f"""{message.author.mention} please add a nickname which has your country and college name (if applicable).""")
                alerted_list.update( {message.author.name : datetime.now()} )
                return
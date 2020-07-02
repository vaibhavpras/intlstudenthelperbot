# bot.py
import os
import nicknamecheck
import similarity
import corpus
import help_response

import discord

from similarity import find_most_similar
from corpus import CORPUS

import asyncio

from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


bot = Bot(command_prefix='!')

msg_id = 0
roles_map = {}
faq_channel = 0
is_faq_enabled = True

def isQuestion(text):
    question_words = ['What', 'When', 'How', 'Where', 'Who', '?']
    question_words = [item.lower() for item in question_words] 
    found = any(ele in text.lower() for ele in question_words)
    return(found)


def answer_question(text):
    question = text
    answer = find_most_similar(question)

    final_answer = ''
    final_question = ''

    if answer['score'] > 0.6:
        print(answer['score'])
        final_answer = answer['answer']
        final_question = answer['question']

    return final_answer, final_question  
        

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.guilds}')

    
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if (message.author.bot):
        return 

    if (message.content.startswith('-')):
        return    

    await nicknamecheck.nicknameCheck(message)   

    if isQuestion(message.content) and int(message.channel.id) == int(faq_channel) and is_faq_enabled:
        (answer_text, question_text) = answer_question(message.content)

        if answer_text:
            botmessage = await message.channel.send(f"""Do you want the answer to: {question_text} """)
            
            await botmessage.add_reaction('\N{THUMBS UP SIGN}')
            await botmessage.add_reaction('\N{THUMBS DOWN SIGN}')

            def checkUp(reaction, user):
                return user == message.author and (str(reaction.emoji) == '\N{THUMBS UP SIGN}' or str(reaction.emoji) == '\N{THUMBS DOWN SIGN}')

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=checkUp)
            except asyncio.TimeoutError:
                await botmessage.delete()
            else:
                print(reaction.emoji)
                if reaction.emoji == '\N{THUMBS UP SIGN}':
                    await botmessage.delete()
                    await message.channel.send(answer_text)

                elif reaction.emoji == '\N{THUMBS DOWN SIGN}':
                    await botmessage.delete()
                    await message.channel.send("Sorry I could not find the answer to your question :( \nPlease ask your question in other channels")


@bot.command(name = "add_country", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_country(ctx, arg):
    with open('countries.txt', 'a') as f:
        f.write(f"""\n{arg}""")
    print(f"""Added {arg} to the list of countries""")
    await ctx.channel.send(f"""Added {arg} to the list of countries""")

@add_country.error
async def add_country_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


@bot.command(name = "add_role_message", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_role_msg(ctx, arg):
    global msg_id
    msg_id = arg 
    print(f"""Assigned {arg} as role_message id""")
    await ctx.channel.send(f"""Assigned {arg} as role_message id""")

@add_role_msg.error
async def add_role_msg_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.command(name = "add_role_emoji", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_role_emoji(ctx, arg1: discord.Emoji, arg2):
    global roles_map
    roles_map.update({arg1.name: arg2})  
    print(f"""Assigned {arg1} to role: {arg2}""")
    await ctx.channel.send(f"""Assigned {arg1} to role: {arg2}""")

@add_role_emoji.error
async def add_role_emoji_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.command(name = "set_faq_channel", pass_context=True)
@has_permissions(manage_roles=True)  
async def set_faq_channel(ctx, arg):
    global faq_channel
    faq_channel = arg 
    print(f"""Assigned {arg} as faq_channel id""")
    await ctx.channel.send(f"""Assigned {arg} as faq_channel id""")

@set_faq_channel.error
async def set_faq_channel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.command(name = "faq_enabled", pass_context=True)
@has_permissions(manage_roles=True)  
async def faq_enabled(ctx, arg):
    if arg.lower() == 'true':
        global is_faq_enabled
        faq_enabled = True
    elif arg.lower() == 'false':
        global is_faq_enabled
        faq_enabled = False
    else:
        await ctx.send('Plase type the command followed by True/False. DO NOT USE QUOTES')
    print(f"""Faq enabled: {arg}""")
    await ctx.channel.send(f"""Faq enabled: {arg}""")

@faq_enabled.error
async def faq_enabled_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.command(name = "adminhelp", pass_context=True)
@has_permissions(manage_roles=True)  
async def adminhelp(ctx):
    await ctx.channel.send(help_response.halp)

@adminhelp.error
async def adminhelp(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == int(msg_id):
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = discord.utils.get(guild.roles, name = roles_map[payload.emoji.name])

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("Role Added!")

@bot.event
async def on_raw_reaction_remove(payload):

    if payload.message_id == int(msg_id):
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = discord.utils.get(guild.roles, name = roles_map[payload.emoji.name])

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("Role removed!")


  
bot.run(os.environ['DISCORD_TOKEN']) 
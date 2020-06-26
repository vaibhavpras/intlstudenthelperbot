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

msg_id = 0

roles_map = {}

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


@bot.command(name = "add_role_msg", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_role_msg(ctx, arg):
    global msg_id
    msg_id = arg 

@add_role_msg.error
async def add_role_msg_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")

@bot.command(name = "add_role_emoji", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_role_emoji(ctx, arg1, arg2):
    global roles_map
    roles_map.update({arg1: arg2})  

@add_role_msg.error
async def add_role_emoji_error(ctx, error):
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

        print(payload.emoji.name)
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = discord.utils.get(guild.roles, name = roles_map[payload.emoji.name])

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("Role removed!")
            

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'{bot.guilds}')

    
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    await nicknamecheck.nicknameCheck(message)       
    
bot.run(TOKEN)
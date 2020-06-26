import json
import discord

from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

#bot = Bot(command_prefix='!')

msg_id = 0

@bot.command(name = "add_role_message", pass_context=True)
@has_permissions(manage_roles=True)  
async def add_role_msg(ctx, arg):
    msg_id = arg 
    print("KK")    

@add_role_msg.error
async def add_role_msg(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == msg_id:
        print(payload.emoji.name)
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("done")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 'id':
        print(payload.emoji.name)

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("done")


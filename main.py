import discord
import random
from discord.ext import commands
from discord.ext.commands import Bot
from discord.flags import Intents
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv('Discord_Token')
channel_general = 848863747891658786


intents = discord.Intents().default()
intents.members =True
client=commands.Bot(command_prefix="!",intents=intents)


def WelcomeMessage():
    messages= ['Welcome Boss! I hope you are going to have a great time with us. So happy to have you among us',
                'Welcome! We are honored to receive you like your presence is crucial!',
                'It is our great pleasure to have you on board! A hearty welcome to you!',
                'We value our customers more than anything, and your satisfaction is what we aim for! Welcome to you! Thank you for visiting us!']
    return random.choice(messages)

@client.event
async def on_ready():
    dbase =sqlite3.connect('data.sqlite')    
    cursor = dbase.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data(
            member_id INT,
            name TEXT
            )
    ''')
    print(f"We have logged in as {client.user}")
    print("Database activated")


async def on_member_join(member):
    guild = client.get_guild(channel_general)
    channel = guild.get_channel(channel_general)
    await channel.send(f"Welcome to the new world {member.mention} :waving: \n Hope to see you at Frontline") 
    await member.send(str(WelcomeMessage()))

      
@client.event
async def on_raw_reaction_add(reaction):
    channel=client.get_channel(reaction.channel_id)
    channel2=client.get_channel(channel_general)
    message=await channel.fetch_message(reaction.message_id)
    emoji=reaction.emoji.name
    await channel2.send(f"{reaction.member.name} reacted to {message.author.name}'s message with {emoji}")


@client.command()
async def role(ctx,*args):
    user=ctx.author
    channel = client.get_channel(channel_general)
    role=await ctx.guild.create_role(name=args[0])
    await user.add_roles(role)
    await channel.send(f'Role {role} was successfully created...Horray!!')

@client.command()
async def add_role(ctx,role:discord.Role,user:discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f'Role  {role.mention} Given to {user.mention}')

@client.command()
async def remove_role(ctx,role:discord.Role,user:discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f'Role {role.mention} removed from {user.mention}')

@client.command()
async def register(ctx,user: discord.User):
    dbase = sqlite3.connect('data.sqlite')
    cursor = dbase.cursor()

    cursor.execute(f"SELECT name FROM data WHERE member_id ={user.id}")
    result =cursor.fetchone()
    if result is None:
        sql =(" INSERT INTO data(member_id,name) VALUES(?,?)" )
        val1=(user.id,user.name)
        cursor.execute(sql,val1)
        await ctx.channel.send(f"User added to the database \n Name: {user.name}\n UserID: {user}\n Status: Success")

    else:
        await ctx.channel.send(f"User already exist \n Name:{user} \n Name:{user.name}")



    dbase.commit()
    cursor.close()
    dbase.close()


@client.command()
@commands.has_role("admin") 
async def names(ctx):
    dbase = sqlite3.connect('data.sqlite')
    cursor = dbase.cursor()


    cursor.execute(f"SELECT name FROM data")
    result =cursor.fetchall()
    for events in result:       
        for content in events:
            await ctx.channel.send(content)


    cursor.close()
    dbase.close()

@client.event
async def on_comman_error(ctx,error):
    pass

client.run(Token)
import discord
import random
from discord.ext import commands
from discord.ext.commands import Bot
import msg_content
from discord.flags import Intents
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv('Discord_Token')

intents = discord.Intents().default()
intents.members =True
client=commands.Bot(command_prefix="!",intents=intents)


def WelcomeMessage():
    messages= msg_content.melcow.message()
    return random.choice(messages)


@client.event
async def on_ready():
    db =sqlite3.connect('data.sqlite')    
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data(
            member_id INT,
            name TEXT
            )
    ''')
    print("Database = active")
    print("We have logged in as {0.user}".format(client))


async def on_member_join(member):
    guild = client.get_guild(848863747891658786)
    channel = guild.get_channel(848863747891658786)
    await channel.send("Welcome to the new world mr {} :waving: ".format(member.mention)) 
    await member.send(str(WelcomeMessage()))



        
@client.event
async def on_raw_reaction_add(reaction):
    channel=client.get_channel(reaction.channel_id)
    channel2=client.get_channel(848863747891658786)
    message=await channel.fetch_message(reaction.message_id)
    emoji=reaction.emoji.name
    await channel2.send(f"{reaction.member.name} reacted to {message.author.name}'s message with {emoji}")


@client.command()
async def role(ctx,*args):
    user=ctx.author
    channel = client.get_channel(848863747891658786)
    role=await ctx.guild.create_role(name=args[0])
    # print(f'The {role} role was suscessfully created by {user}')
    await user.add_roles(role)
    await channel.send(f'{role} was successfully created...')


@client.command()
async def register(ctx,user: discord.User):
    db = sqlite3.connect('data.sqlite')
    cursor = db.cursor()

    cursor.execute(f"SELECT name FROM data WHERE member_id ={user.id}")
    result =cursor.fetchone()
    if result is None:
        sql =(" INSERT INTO data(member_id,name) VALUES(?,?)" )
        val1=(user.id,user.name)
        cursor.execute(sql,val1)
        await ctx.channel.send(f"The user added to the database \n Username: {user.name}\n UserID: {user}\n Status: Success")

    else:
        await ctx.channel.send(f"The user already exist \n Username:{user} \n Name:{user.name}")



    db.commit()
    cursor.close()
    db.close()


@client.command()
@commands.has_role("admin") 
async def names(ctx):
    db = sqlite3.connect('data.sqlite')
    cursor = db.cursor()


    cursor.execute(f"SELECT name FROM data")
    result =cursor.fetchall()
    for i in result:       
        for j in i:
            await ctx.channel.send(j)


    cursor.close()
    db.close()

@client.event
async def on_comman_error(ctx,error):
    pass

client.run(Token)
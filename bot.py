from discord import channel, message
from discord.utils import get
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('Discord_Token')

client = commands.Bot(command_prefix='!',help_command=None)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    str_name = str(message.author).split("#")
    str_act = str_name[0]
    
    if message.content.startswith('!hello'):
        await message.channel.send('Hey...\n'+ str_act +"\nHow you Doin..??")
    if message.content.startswith('!greet'):
        str_gret = str(message.mentions).split(" ")
        str_gret = str_gret[2].split("'")
        str_gret = str_gret[1]
        await message.channel.send(str_act +" Greeted "+str_gret)
    if message.content.startswith("💐"):
        str_gret = str(message.mentions).split(" ")
        str_gret = str_gret[2].split("'")
        str_gret = str_gret[1]
        await message.channel.send(" Greetings "+str_gret +" 💐\n"+"\t~"+str_act)


        

@client.command()
async def add_role(ctx,role:discord.Role,user:discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f'Role  {role.mention} Given to {user.mention}')




client.run(TOKEN)
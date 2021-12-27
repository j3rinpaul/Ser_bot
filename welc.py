import discord
from discord.ext import commands
from discord.utils import get 
import os
from dotenv import load_dotenv

load_dotenv()

TOKE = os.getenv('Dis_3rd')
 
bot_r = commands.Bot(command_prefix='#',help_command=None)

@bot_r.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}!") 

bot_r.run(TOKE)


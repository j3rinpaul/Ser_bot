import discord
from discord.ext import commands
from discord.utils import get 
import os
from dotenv import load_dotenv

load_dotenv()

TOK = os.getenv('Dis_test')



bot = commands.Bot(command_prefix='$',help_command=None)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command()
async def add_role(ctx,role:discord.Role,user:discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f'Role  {role.mention} Given to {user.mention}')

@bot.command()
async def remove_role(ctx,role:discord.Role,user:discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f'Role {role.mention} removed from {user.mention}')


bot.run(TOK)
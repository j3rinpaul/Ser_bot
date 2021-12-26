from discord import channel, message
import discord.ext
import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('Discord_Token')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')


    async def on_message(self,message):
        if message.author == self.user:
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
            await message.channel.send(str_act +" Greeted "+str_gret)


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f"Welcome {member.mention} to {guild.name}!"
            await guild.system_channel.send(to_send) 




bot = MyClient()
bot.run(TOKEN)
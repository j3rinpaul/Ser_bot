import discord

bot = discord.Bot()

#function to greet new user
@bot.event
async def on_member_join(member):
    await bot.send_message(member, "Welcome to the server, " + member.mention + "!")


#register a user with a role 
@bot.event
async def on_message(message):
    if message.content.startswith("!register"):
        role = discord.utils.get(message.server.roles, name="Registered")
        await bot.add_roles(message.author, role)
        await bot.send_message(message.channel, "You have been registered!")

#if already registered, give warning
@bot.event
async def on_message(message):
    if message.content.startswith("!register"):
        role = discord.utils.get(message.server.roles, name="Registered")
        if role in message.author.roles:
            await bot.send_message(message.channel, "You are already registered!")

#function to sent message to channel when a user gave reaction to a message
@bot.event
async def on_reaction_add(reaction, user):
    for reaction in reaction.message.reactions:
        await bot.send_message(reaction.message.channel, "{} Gave reaction to, {}!".format(user.name,user.mention))

#function to retrive names in database when asked by a user of certain role
@bot.event
async def on_message(message):
    if message.content.startswith("!names"):
        role = discord.utils.get(message.server.roles, name="Registered")
        if role in message.author.roles:
            await bot.send_message(message.channel, "Names of users with the role Registered:")
            for member in message.server.members:
                if role in member.roles:
                    await bot.send_message(message.channel, member.name)



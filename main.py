import discord
import json

with open('key.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is logged in.")

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 942313993794637824: # paste message id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            # member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            member = payload.member
            if member is not None:
                await member.add_roles(role)
            else:
                print("Error: Member not found.")
        else:
            print("Error: Role not found.")

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 942313993794637824:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            # member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            member = payload.member
            if member is not None:
                await member.remove_roles(role)
            else:
                print("Error: Member not found.")
        else:
            print("Error: Role not found.")

client.run(TOKEN)
import discord
from discord.ext import commands
import json

with open('key.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

client = commands.Bot(command_prefix="!")

@client.command()
async def server(ctx):
    ctx.guild


client.run(TOKEN)
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
async def on_message(message):
    if message.content == "ping":
        await message.channel.send('pong')

client.run(TOKEN)
import discord
from discord.ext import commands, tasks
from itertools import cycle
from word_list import illegal_words
import json

with open('key.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

client = commands.Bot(command_prefix=".")
status = cycle([
    "bothub.com",
    "hottybotty.com",
    "botsnthots.com",
    "mailorderbots.com",
    "onlybots.com",
    "christianbotmingle.com",
    "botharmony.com",
    "botslist.org",
    "tinder. I'm desperate.",
    "anyone but rob"
])


@client.event
async def on_ready():
    change_status.start()
    print("Bot is logged in.")


@tasks.loop(hours=1)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))


@client.event
async def on_message(message):
    if any(word in message.content for word in illegal_words):
        channel = client.get_channel(858032902506938378)
        if message.channel != channel:
            await message.delete()
            await message.channel.send("""That word is not allowed to be used! Continued use of banned words will lead to a timeout or permanent ban from the server. Tread carefully.""")
            await channel.send(f"{message.author} has been warned for their word choice - '{message.content}'")
    else:
        await client.process_commands(message)


@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    guild_id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    member_count = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.dark_purple()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

client.run(TOKEN)

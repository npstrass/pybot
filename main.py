import asyncio

import discord
from discord.ext import commands
from discord.utils import get
import json
from twitch import twitch_users as tu

with open('key.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

intents = discord.Intents.all()

client = commands.Bot(command_prefix=".", intents=intents)

ticketNumber = 1


@client.event
async def on_ready():
    print("Pybot logged in")


@client.event
async def on_member_join(member):
    alert_channel = client.get_channel(858032902506938378)
    welcome_channel = client.get_channel(859490311897350144)
    embed = discord.Embed(
        title="New User",
        description=f"{member} has joined the server.",
        color=discord.Color.green()
    )
    await welcome_channel.send(f"Welcome, {member.mention}, to our community! Glad to have you.")
    await alert_channel.send(embed=embed)


@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    guild_id = str(ctx.guild.id)
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
    embed.add_field(name="Member Count", value=member_count, inline=True)

    await ctx.reply(embed=embed)


@client.command()
async def announce(ctx, *, message):
    send_channel = client.get_channel(545149173872328747)
    await send_channel.send(message)


@client.command()
@commands.has_role('mods')
async def clear(ctx, amount=5):
    alert_channel = client.get_channel(858032902506938378)
    embed = discord.Embed(
        title="Messages Cleared",
        description=f"{ctx.author} has cleared {amount} messages from {ctx.channel.mention}"
    )
    await ctx.channel.purge(limit=amount)
    await alert_channel.send(embed=embed)


@client.command()
@commands.has_role('mods')
async def kick(ctx, member: discord.Member, *, reason=None):
    alert_channel = client.get_channel(858032902506938378)
    embed = discord.Embed(
        title="Member kicked",
        description=f"{ctx.author} has kicked {member} for the following reason:",
        color=discord.Color.gold()
    )
    embed.add_field(name="Reason", value=reason, inline=True)
    try:
        await member.send(
            "You've been kicked from the server. You can use https://discord.gg/arcz8ctYaW to rejoin the server. "
            "Please revisit the rules and follow them going forward or a permanent ban will follow. Thank you. "
        )
    except:
        await alert_channel.send(
            f"Error: {member} was kicked but no message was sent. DMs for this user are closed."
        )
    await member.kick(reason=reason)
    await alert_channel.send(embed=embed)


@client.command()
@commands.has_role('mods')
async def ban(ctx, member: discord.Member, *, reason=None):
    alert_channel = client.get_channel(858032902506938378)
    embed = discord.Embed(
        title="Member banned",
        description=f"{ctx.author} has banned {member} for the following reason:",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason", value=reason, inline=True)
    await member.ban(reason=reason)
    await alert_channel.send(embed=embed)


@client.command()
@commands.has_role('mods')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            alert_channel = client.get_channel(858032902506938378)
            embed = discord.Embed(
                title="Member unbanned",
                description=f"{ctx.author} has unbanned {member}",
                color=discord.Color.light_grey()
            )
            await ctx.guild.unban(user)
            await alert_channel.send(embed=embed)
            return


@client.command()
@commands.has_role('mods')
async def softban(ctx, member: discord.Member, *, reason=None):
    alert_channel = client.get_channel(858032902506938378)
    embed = discord.Embed(
        title="Member soft banned",
        description=f"{ctx.author} has soft banned {member} for the following reason:",
        color=discord.Color.orange()
    )
    embed.add_field(name="Reason", value=reason, inline=True)
    try:
        await member.send(
            "You've been soft banned as a warning. You can use https://discord.gg/arcz8ctYaW to rejoin the server. "
            "Please revisit the rules and follow them. Thank you. "
        )
    except:
        await alert_channel.send(
            f"Error: {member} was soft banned but no message was sent. DMs for this user are closed."
        )
    await member.ban(reason=reason)
    await member.unban()
    await alert_channel.send(embed=embed)
    return


@client.command()
async def live(ctx, member: discord.Member):
    send_channel = client.get_channel(545149173872328747)
    for i in tu:
        if i[0] == str(member):
            await ctx.message.delete()
            await send_channel.send(f'🔴 {member.display_name} is going live! https://twitch.tv/{i[1]} 🔴')
    await member.send("If your announcement was not made, it may be because you aren't a part of our streamer list. "
                      "Please submit a `.ticket` and a mod will review your request! Thanks!")


@client.command()
async def ticket(ctx):
    global ticketNumber
    ticketNumber = str(ticketNumber)
    guild = ctx.message.guild
    author = ctx.author
    mod_role = get(guild.roles, name="mods")
    name = str(f'help ticket 00{ticketNumber}')
    await ctx.message.delete()
    channel = await guild.create_text_channel(f"{name} - {author.nick}", topic="AHHHHH YOU NEED HELP!")
    await channel.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
    await channel.set_permissions(mod_role, read_messages=True, send_messages=True, connect=True)
    await channel.set_permissions(author, read_messages=True, send_messages=True, connect=True)
    await channel.send(f'{author.mention}, please type your help request below and one of our {mod_role.mention} will assist you as soon as they can!')
    ticketNumber = int(ticketNumber) + 1


@client.command()
@commands.has_role('mods')
async def close(ctx):
    name = ctx.channel.name
    guild = ctx.message.guild
    channel = discord.utils.get(guild.channels, name=name)
    if 'help-ticket' in str(name):
        await channel.delete()
    else:
        await ctx.send('channel cannot be deleted')


@client.command()
async def vote(ctx):
    embed = discord.Embed(
        title="Vote for the server!",
        description="Support our server by voting for us on Discord Street! :muscle:",
        color=discord.Color.teal()
    )
    embed.add_field(name="URL", value="https://discord.st/vote/nosecommunity/", inline=True)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send("pong")


client.run(TOKEN)

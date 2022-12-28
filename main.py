import asyncio

import discord
from discord.ext import commands
from discord.utils import get
from word_list import illegal_words
import json

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


@client.event
async def on_message(message):
    if any(word in message.content for word in illegal_words):
        channel = client.get_channel(858032902506938378)
        embed = discord.Embed(
            title="Message deleted",
            color=discord.Color.purple()
        )
        embed.add_field(name="User", value=message.author, inline=True)
        embed.add_field(name="Channel", value=message.channel, inline=True)
        embed.add_field(name="Message removed", value=message.content, inline=True)

        if message.channel != channel:
            await message.delete()
            await message.channel.send(
                "That word is not allowed to be used! Continued use of banned words will lead to a timeout or \n"
                "permanent ban from the server. Tread carefully.")
            await channel.send(embed=embed)
    else:
        await client.process_commands(message)


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
@commands.has_role('mods')
async def announce(ctx, member: discord.Member, user, *, message):
    announce_channel = client.get_channel(545149173872328747)
    name = member.display_name
    pfp = member.avatar_url
    embed = discord.Embed(
        title=f"{name} is going live 🔴",
        description=f"@everyone {message}",
        color=discord.Color.purple()
    )
    embed.set_image(url=pfp)
    embed.add_field(name="Link", value=f"https://twitch.tv/{user}", inline=True)
    try:
        await announce_channel.send(embed=embed)
    except:
        await ctx.reply(f"Error: Make sure you use the format '.announce @member link message'")


# @client.command()
# async def mod(ctx, *, message):
#     send_channel = client.get_channel(944082391645978665)
#     author = str(ctx.author)
#     nick = str(ctx.author.nick)
#     channel = str(ctx.channel)
#     text = str(message)
#     message_url = ctx.message.jump_url
#
#     embed = discord.Embed(
#         title="You got mail",
#         description=f"{nick} has sent a message to mod mail",
#         color=discord.Color.dark_teal()
#     )
#     embed.add_field(name="Message", value=text, inline=True)
#     embed.add_field(name="Author", value=author, inline=True)
#     embed.add_field(name="In channel", value=channel, inline=True)
#     embed.add_field(name="Url", value=message_url, inline=True)
#
#     await ctx.reply("Your mail has been sent! A mod will get back to you as soon as possible.")
#     await send_channel.send(embed=embed)


@client.command()
async def ticket(ctx):
    global ticketNumber
    ticketNumber = str(ticketNumber)
    guild = ctx.message.guild
    author = ctx.author
    mod_role = get(guild.roles, name="mods")
    name = str(f'ticket #{ticketNumber}')
    await ctx.message.delete()
    category = await ctx.guild.create_category(name)
    await category.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
    await category.set_permissions(author, read_messages=True, send_messages=True, connect=True)
    await category.set_permissions(mod_role, read_messages=True, send_messages=True, connect=True)
    channel = await guild.create_text_channel(f"{author.nick}'s ticket", topic="AHHHHH YOU NEED HELP!", category=category, sync_permissions=True)
    await channel.send(f'{author.mention}, please type your help request below and one of our {mod_role.mention} will assist you as soon as they can!')
    ticketNumber = int(ticketNumber) + 1


@client.command()
async def drag(ctx):
    if ctx.channel.id == 969842261028397066:
        send_channel = client.get_channel(969842629317636116)
        voice_channel = client.get_channel(943693630349148200)
        author = ctx.author
        nick = str(ctx.author.nick)

        embed = discord.Embed(
            title="Drag request",
            description=f"{nick} is requesting a drag down to a live room",
            color=discord.Color.gold()
        )
        embed.add_field(name="Mention", value=author.mention, inline=True)
        embed.add_field(name="Author", value=author, inline=True)

        await ctx.reply("Your drag request has been sent.")
        msg = await send_channel.send(embed=embed)
        await msg.add_reaction("✅")

        def check(reaction, user):
            return user != msg.author and str(reaction.emoji) == '✅'

        try:
            reaction, user = await client.wait_for('reaction_add', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.reply("Your request timed out")
        else:
            try:
                await author.move_to(voice_channel)
                await send_channel.send(f"{user.nick} has dragged {nick} to live room 1 {reaction}")
            except:
                await ctx.reply("Make sure you're in a voice chat! Try again.")
                await send_channel.send("Error. Incorrect reaction or user not in voice chat")
    else:
        await ctx.reply("That command is not valid here. Please go to channel <#969842261028397066>")
        await ctx.message.delete()


@client.command()
@commands.has_role('mods')
async def d1(ctx):
    try:
        drag_channel = client.get_channel(944411038307213332)
        member_to_drag_1 = drag_channel.members[0]
        voice_channel = client.get_channel(943693630349148200)
        await member_to_drag_1.move_to(voice_channel)
    except:
        print("error moving member to live room 1")
    await ctx.message.delete()


@client.command()
@commands.has_role('mods')
async def b(ctx, member: discord.Member = None):
    try:
        await member.move_to(None)
    except:
        print("error booting member")
    await ctx.message.delete()


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
@commands.has_permissions(administrator=True)
async def instruct(ctx):
    embed = discord.Embed(
        title="Mod commands:",
        description="Below are the commands mods can use to keep the server in check",
        color=discord.Color.dark_grey()
    )
    embed.add_field(
        name=".clear",
        inline=True,
        value="The clear command by itself will erase the previous 5 lines of messages. You can indicate a quantity "
              "with .clear 10."
    )
    embed.add_field(
        name=".kick",
        value="The kick command will kick the member tagged after. For example, .kick @rob. Any text following the "
              "user will indicate the reason for the kick. If you kick someone, please provide a reason.",
        inline=True
    )
    embed.add_field(
        name=".ban",
        value="The ban command will permanently ban the member tagged after. For example, .ban @rob. Any text "
              "following the user will indicate the reason for the ban. If you ban someone, you MUST provide a reason.",
        inline=True
    )
    embed.add_field(
        name=".unban",
        value="The unban command will unban the member tagged after. For example, .unban @rob.",
        inline=True
    )
    embed.add_field(
        name=".softban",
        value="The softban command will ban and immediately unban the member tagged after. Can be used to warn and "
              "will erase a members messages server wide. For example .softban @rob. Any text following the user will "
              "indicate the reason for the softban. If you softban, you MUST provide a reason.",
        inline=True)
    embed.add_field(
        name=".vote",
        value="The vote command will prompt in the channel used the url to vote. Please use this to promote voting, "
              "engagement, and growth within the server. All members can use this command.",
        inline=True
    )
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send("pong")


client.run(TOKEN)

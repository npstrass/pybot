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
    "amazing world of gumball",
    "hot tub streams",
    "adventure time",
    "south park",
    "rick and morty",
    "bob's burgers",
    "solar opposites",
    "teen titans go",
    "archer",
    "anyone but rob"
])


@client.event
async def on_ready():
    change_status.start()
    print("Bot is logged in.")


@tasks.loop(hours=3)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))


@client.event
async def on_message(message):
    if any(word in message.content for word in illegal_words):
        channel = client.get_channel(858032902506938378)
        embed = discord.Embed(
            title="Message deleted",
            color=discord.Color.dark_theme()
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
@commands.has_role('mods' or 'staff' or 'super staff')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_role('mods' or 'staff' or 'super staff')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
@commands.has_role('mods' or 'staff' or 'super staff')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


@client.command()
@commands.has_role('mods' or 'staff' or 'super staff')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


@client.command()
@commands.has_role('mods' or 'staff' or 'super staff')
async def softban(ctx, member: discord.Member, *, reason=None):
    channel = client.get_channel(858032902506938378)
    await member.ban(reason=reason)
    await member.unban()
    await channel.send(
        f"{member} flew close to the sun... but not too close. Soft banning to warn and remove messages."
    )
    return


@client.command()
async def mod(ctx, *, message):
    send_channel = client.get_channel(944082391645978665)
    author = str(ctx.author)
    nick = str(ctx.author.nick)
    channel = str(ctx.channel)
    text = str(message)
    message_url = ctx.message.jump_url

    embed = discord.Embed(
        title="You got mail",
        description=f"{nick} has sent a message to mod mail",
        color=discord.Color.random()
    )
    embed.add_field(name="Message", value=text, inline=True)
    embed.add_field(name="Author", value=author, inline=True)
    embed.add_field(name="In channel", value=channel, inline=True)
    embed.add_field(name="Url", value=message_url, inline=True)

    await ctx.send("Your mail has been sent! A mod will get back to you as soon as possible.")
    await send_channel.send(embed=embed)


@client.command()
async def vote(ctx):
    embed = discord.Embed(
        title="Vote for the server!",
        description="Support our server by voting for us on Discord Street! :muscle:",
        color=discord.Color.teal()
    )
    embed.add_field(name="URL", value="https://discord.st/vote/nosecommunity/", inline=True)
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


client.run(TOKEN)

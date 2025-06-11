"""
Discord Bot for Server Management

This bot provides several key features:
1. Member Welcome: Sends a custom welcome message to new members
2. Word Filtering: Monitors messages for inappropriate content and issues warnings
3. Role Management: Allows users to self-assign the 'SilverBack' role using !assign
4. Basic Interaction: Responds to !hello command with a friendly message

Required Environment Variables:
- DISCORD_TOKEN: Bot authentication token (must be set in .env file)

Bot Permissions Required:
- message_content: To read message content
- members: To access member information and manage roles

- William Peebles
- 06/10/2025
"""
from binascii import a2b_qp

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("DISCORD_TOKEN not found in .env file")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "SilverBack"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server watermelon baboon kool aid drinking banana vine swinging chicken lover{member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # First process commands, so they work properly
    await bot.process_commands(message)

    # Then check for bad words
    list_of_bad_words = ["shit"]

    for s in list_of_bad_words:
        if s in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} - don't use that word monkey one more and you're going 3 days in the hole!")
            return

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hey {ctx.author.mention}! You're the greatest monkey!")

#!assign
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Know your role and shut your mouth monkey, this role doesn't exist.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Know your role and shut your mouth monkey, this role doesn't exist.")
# !dm ....
@bot.command()
async def dm(ctx, *,msg):
    await ctx.author.send(f"You said {msg}")
#!reply to this
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message monkey!")

@bot.command()
async def poll(ctx,*, question):
    embed = discord.Embed(title="New Poll", description="React to this message to vote!", color=0x00ff00)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

#!secret
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club monkey!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have permission to do that monkey!")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
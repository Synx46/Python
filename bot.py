import discord
import random
import time
import asyncio
from discord.ext import commands, tasks
from random import choice


TOKEN = "#"

client = discord.Client()

status = ['Travis Bott', 'BotTube', 'Cyberbot 2069', 'Serving master']

responses = [
    "Absolutely Not",
    "Yes",
    "My master denies",
    "Seems not",
    "I dont have time for this nonsense",
]

hello = (
    "hello",
    "hi",
    "sup",
    "HI",
    "Hi",
    "hI",
    "Hello",
    "HELLO"
    "Hello bot"
)



heads = [
    "heads",
    "tails"
]

@client.event


async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/ping"):
        await message.channel.send(f'***Latency***: {round(client.latency *1000)}ms')


    if message.content.startswith("/say"):
        mes = message.content.split()
        output = ""
        for word in mes[1:]:
            output += word
            output += " "
        await message.channel.send(output)
        await message.delete()

    if message.content.startswith("/heysynx"):
        await message.channel.send(random.choice(responses))

    if message.content.startswith("/help"):
        embed = discord.Embed(title="__Commands__", color=0x98ff00)
        embed.add_field(name="/help", value="Shows this message")
        embed.add_field(name="/ping", value="Shows latency ")
        embed.add_field(name="/say", value="Makes the bot say a message")
        embed.add_field(name="/heysynx", value="Ask the bot a question")
        await message.channel.send(content=None, embed=embed)

    if message.content.startswith(hello):
        channel = message.channel
        await channel.send("Hey")
        await channel.send("Do you want to play heads or tails")

        def check(m):
            return m.content in ("Yes", "sure", "yes", "Sure", "I hope so")

        msg = await client.wait_for('message', check=check)
        await channel.send("Ok \n"
                           "I pick \n")
        await channel.send(random.choice(heads))
        await channel.send("The winner is.....")
        await channel.send(random.choice(heads))




@client.event
async def on_ready():
    change_status.start()
    print('Running')

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


client.run(TOKEN)


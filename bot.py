import discord
import random
import time
import asyncio
TOKEN = "OTExMjU5MTI2MzIyMDQ5MDU1.YZeyMg.vtHuZCCgn5Z4R8sUnk-N9q1Vssw"

client = discord.Client()

responses = [
    "Absolutely Not",
    "Yes",
    "My master denies",
    "It seems likely",
]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/ping"):
        await message.channel.send("Pong")

    if message.content.startswith("/say"):
        mes = message.content.split()
        output = ""
        for word in mes[1:]:
            output += word
            output += " "
        await message.channel.send(output)
        await message.delete()



@client.event
async def on_ready():
    print('Running')


client.run(TOKEN)

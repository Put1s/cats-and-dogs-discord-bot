import asyncio
import logging
import random
import requests

import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "YOUR BOT TOKEN"


class CatsAndDogsBot(discord.Client):
    def __init__(self, intents=""):
        super().__init__(intents=intents)
        self.cats_marks = ['кот', 'кош', 'котик', 'котёнок', 'котята', 'cat', 'kitt']
        self.dogs_marks = ['собак', 'собач', 'пёс', 'псы', 'dog']

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        cats = False
        dogs = False
        for mark in self.cats_marks:
            if mark in message.content.lower():
                cats = True
                break
        for mark in self.dogs_marks:
            if mark in message.content.lower():
                dogs = True
                break
        if cats:
            response = requests.get('https://api.thecatapi.com/v1/images/search')
            url = response.json()[0]["url"]
            print(url)
            await message.channel.send(url)
        if dogs:
            response = requests.get('https://dog.ceo/api/breeds/image/random')
            url = response.json()["message"]
            print(url)
            await message.channel.send(url)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = CatsAndDogsBot(intents=intents)
client.run(TOKEN)

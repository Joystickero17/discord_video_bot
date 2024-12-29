import discord
from dotenv import load_dotenv
import os
from utils import save_facebook_video, save_video_instagram, save_video_tiktok
import random

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
EMAIL_SUPPORT = "augustocarrillo20@gmail.com"


intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True
class Client(discord.Client):

    async def on_ready(self):
        print(self.guilds)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!help'):
            msg= "!face <url> para videos de facebook o instagram\n!tk <url> para videos de tiktok\nalternativamente con !insta <url> descargas videos de instagram puede que más lento"
            await message.channel.send(msg)
        if message.content.startswith('!face') or message.content.startswith('!ahpues'):
            try:
                name = save_facebook_video(message.content.split(' ')[1])
                await message.channel.send("here is your video :)", file=discord.File(name))
                os.remove(name)
            except Exception as e:
                print(e)
                await message.channel.send("Ah ocurrido un error por favor contactar a {}".format(EMAIL_SUPPORT))
        if message.content.startswith('!tk') or message.content.startswith('!ahvaina'):
            try:
                name = save_video_tiktok(message.content.split(' ')[1])
                await message.channel.send("here is your video :)", file=discord.File(name))
                os.remove(name)
            except Exception as e:
                print(e)
                await message.channel.send("Ah ocurrido un error por favor contactar a {}".format(EMAIL_SUPPORT))
        if message.content.startswith('!semeruca') or message.content.startswith('!insta'):
            try:
                name = save_video_instagram(message.content.split(' ')[1])
                await message.channel.send("here is your video :)", file=discord.File(name))
                os.remove(name)
            except Exception as e:
                print(e)
                await message.channel.send("Ah ocurrido un error por favor contactar a {}".format(EMAIL_SUPPORT))
            # await message.channel.send('quetepasa!')


client = Client(intents=intents)
client.run(token)
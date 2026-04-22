import discord
from dotenv import load_dotenv
import os
from utils import DownloaderFactory, InvalidUrlParseError, ParserNotFoundError

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
        downloader = DownloaderFactory().get_downloader(message)
        try:
            name = downloader.download()
        except ParserNotFoundError as e:
            await message.channel.send("Ah ocurrido un error")
            return
        except InvalidUrlParseError as e:
            print("Invalid URL")
            return
        await message.channel.send("here is your video :)", file=discord.File(name))
        os.remove(name)
client = Client(intents=intents)
client.run(token)
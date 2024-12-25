import discord
from dotenv import load_dotenv
import os
from utils import save_facebook_video, save_video_instagram, save_video_tiktok
import random

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True
random_messages = [
    "Ah pues ahora soy payaso tuyo",
    "No me creas pues mmwbo",
    "chamo ustedes tienen que estar bien ladillados",
    "Que quieres mldto sapo"
]
class Client(discord.Client):

    async def on_ready(self):
        print(self.guilds)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!conectame'):
            channel = message.author.voice.channel
            voice = await channel.connect()
        if message.content.startswith('wendy cree que ese no es diego'):
            await message.channel.send("dejala quieta, arriba hay un dios")
        if 'ese no es diego' in message.content.lower():
            await message.channel.send(random.choice(random_messages))
        if 'diego' in message.content.lower() and 'ese no es diego' not in message.content.lower():
            await message.channel.send(random.choice(random_messages))
        if message.content.startswith('!help'):
            msg= "!ahpues <url> para videos de facebook\n!ahvaina <url> para videos de tiktok\nNo abusen del bot porque se arrecha y se acuesta a dormir\nSSssssSSssSSS"
            await message.channel.send(msg)
        if message.content.startswith('!ahpues'):
            try:
                name = save_facebook_video(message.content.split(' ')[1])
                await message.channel.send("Aqui está tu video camarada", file=discord.File(name))
                os.remove(name)
            except Exception as e:
                print(e)
                await message.channel.send("Mrc que eso que te pasa!")
        if message.content.startswith('!ahvaina'):
            try:
                name = save_video_tiktok(message.content.split(' ')[1])
                await message.channel.send("Aqui está tu video camarada", file=discord.File(name))
                os.remove(name)
            except Exception as e:
                print(e)
                await message.channel.send("Mrc que eso que te pasa!")
        if message.content.startswith('!semeruca'):
            try:
                name = save_video_instagram(message.content.split(' ')[1])
                await message.channel.send("Aqui está tu video camarada", file=discord.File(name))
                os.remove(name)
            except Exception as e:
                print(e)
                await message.channel.send("Mrc que eso que te pasa!")
            # await message.channel.send('quetepasa!')


client = Client(intents=intents)
client.run(token)
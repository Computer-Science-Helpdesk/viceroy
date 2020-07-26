import discord
from discord.ext import commands
import datetime
import yaml

bot = commands.Bot(command_prefix='--', description='A bot designed to administrate a given discord server.')

def load():
    return yaml.load(open('config.yaml'), Loader=yaml.FullLoader)

def transform(message):
    return message.content

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

@bot.command()
async def save(ctx):
    for channel in ctx.guild.text_channels:
        writeFile = open('{0}-backup-{1}.txt'.format(channel.name, str(datetime.date.today())), 'w', encoding='utf-8')
        async for log in channel.history(limit=None):
            writeFile.write(log.author.name + ': ' + transform(log) + '\n')

@bot.command()
async def configure(ctx):
    save(ctx)
    guild = ctx.guild
    

@bot.command()
async def close(ctx):
    await bot.close()

"""class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}'.format(self.user))

    async def save(self):
        for channel in self.get_all_channels():
            if channel.type == discord.ChannelType.text:
                writeFile = open('{0}-backup.txt'.format(channel.name), 'r')
                for log in channel.history(limit=None):
                    writeFile.write(log.map(transform))

client = MyClient()
client.run(open('token.txt').read())"""
bot.run(open('token.txt').read())
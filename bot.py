import discord
from discord.ext import commands
import datetime
import yaml
import pprint

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
async def ping(ctx):
    config = load()
    await ctx.send('Hello, here is the current config file: ' + pprint.pformat(config))

@bot.command()
async def configure(ctx):
    await save(ctx)
    config = load()
    protectedRoles = config['protectedRoles']
    guild = ctx.guild
    # Remove roles
    roles = guild.roles
    for role in roles:
        if any(role.name == elem for elem in protectedRoles):
            await ctx.send('True')
        else:
            print(role.name)
            await role.delete()
    # Create roles
    for role in config['labeledRoles']:
        await guild.create_role(name=role, hoist=True, mentionable=True)
    for role in config['roles']:
        await guild.create_role(name=role, mentionable=True)
    # Remove channels
    channels = guild.channels
    for channel in channels:
        await channel.delete()
    # Create channels
    for channel in config['channels']:
        channelName = list(channel)[0]
        print(channelName)
        if channel[channelName]['type'] == 'Text':
            await guild.create_text_channel(channelName)
        elif channel[channelName]['type'] == 'Voice':
            await guild.create_voice_channel(channelName)
    # Changes channel permissions
    roles = guild.roles
    channels = guild.channels
    i = 0
    for channel in channels:
        print(config['channels'][i])
        channelName = list(config['channels'][i])[0]
        channelConfig = config['channels'][i][channelName]['permissions']
        for role in channelConfig:
            roleObj = None
            print(role)
            for elem in roles:
                if elem.name == role:
                    roleObj = elem
            if channelConfig[role] == 'all':
                print(discord.Permissions.all())
                channel.set_permissions(roleObj, overwrite=discord.Permissions.all())
            elif channelConfig[role] == 'general':
                print(discord.Permissions.general())
                channel.set_permissions(roleObj, overwrite=discord.Permissions.general())
        i += 1

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
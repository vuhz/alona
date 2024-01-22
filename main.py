from discord.ext import commands
import os , discord, json

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
activity = discord.Activity(name='test', type=discord.ActivityType.watching)

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    activity=activity,
)
bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

with open('config.json', 'r+', encoding='utf-8') as f:
    token = json.loads(f.read())["token"]

bot.run(token)



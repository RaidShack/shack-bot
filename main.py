import config
import discord

from discord.ext import commands

initial_extensions = (
    'cogs.events',
    'cogs.gdrive',
    'cogs.member',
    'cogs.routs',
    'cogs.stats',
)


class RaidShack(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for extension in initial_extensions:
            self.load_extension(extension)


intents = discord.Intents.default()
intents.members = True

client = RaidShack(command_prefix='rs-', intents=intents)
client.run(config.token)

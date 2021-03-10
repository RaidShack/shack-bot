from discord.ext import commands
import config
import discord


class RaidShack(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_extensions = (
            'cogs.events',
            'cogs.gdrive',
            'cogs.member',
            'cogs.routes',
            'cogs.stats',
        )

        for extension in self.initial_extensions:
            self.load_extension(extension)

        self.load_extension('cogs.admin')


intents = discord.Intents.default()
intents.members = True

bot = RaidShack(command_prefix='rs-', intents=intents)
bot.run(config.token)

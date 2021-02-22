import config
import discord
from discord.ext import commands

initial_extensions = (
    'cogs.member',
    'cogs.post',
    'cogs.stats',
)


class RaidShack(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gdrive = config.gdrive

        for extension in initial_extensions:
            self.load_extension(extension)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Pokémon Go"))


intents = discord.Intents.default()
intents.members = True

client = RaidShack(command_prefix='rs-', intents=intents)
client.run(config.token)

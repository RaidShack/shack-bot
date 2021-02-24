import config
import discord
import random
from discord.ext import commands

initial_extensions = (
    'cogs.gdrive',
    'cogs.member',
    'cogs.stats',
)


class RaidShack(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gdrive_folder = config.gdrive_folder
        self.gdrive_api = config.gdrive_api

        for extension in initial_extensions:
            self.load_extension(extension)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Pokémon Go"))

    @staticmethod
    async def on_member_join(member):
        channel = member.guild.system_channel
        welcome_text = [
            "{0} joined the party.",
            "{0} is here.",
            "Welcome, {0}. We hope you brought pizza.",
            "A wild {0} appeared.",
            "{0} just landed.",
            "{0} just slid into the server.",
            "{0} just showed up!",
            "Welcome {0}. Say hi!",
            "{0} hopped into the server.",
            "Everyone welcome {0}!",
            "Glad you're here, {0}.",
            "Good to see you, {0}.",
            "Yay you made it, {0}!",
        ]
        await member.add_roles(member.guild.get_role(config.role_id))
        if channel is not None:
            await channel.send(random.choice(welcome_text).format(member.mention))


intents = discord.Intents.default()
intents.members = True

client = RaidShack(command_prefix='rs-', intents=intents)
client.run(config.token)

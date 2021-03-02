from discord.ext import commands
import config
import discord
import random


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Pokémon Go"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
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


def setup(bot):
    bot.add_cog(Events(bot))

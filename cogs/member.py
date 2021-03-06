from discord.ext import commands
import discord


class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def member(self, ctx):
        members = await ctx.guild.fetch_members(limit=None).flatten()
        async with ctx.typing():
            for member in members:
                if not member.bot:
                    await member.add_roles(discord.utils.get(member.guild.roles, name='Member'))
        await ctx.send('Done add Member role')

    @member.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, you can't run this command")
        else:
            raise error


def setup(bot):
    bot.add_cog(Member(bot))

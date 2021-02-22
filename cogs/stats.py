from discord.ext import commands
import discord


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        members = await ctx.guild.fetch_members(limit=None).flatten()
        member_count = 0
        member_role_count = 0
        instinct_count = 0
        mystic_count = 0
        valor_count = 0
        ign_count = 0
        tc_count = 0
        level_count = 0
        country_count = 0
        profile_count = 0
        for member in members:
            if not member.bot:
                member_count += 1
                for role in member.roles:
                    if role.name == "Member":
                        member_role_count += 1
                    if role.name == "instinct":
                        instinct_count += 1
                    if role.name == "mystic":
                        mystic_count += 1
                    if role.name == "valor":
                        valor_count += 1
                    if role.name == "ign":
                        ign_count += 1
                    if role.name == "tc":
                        tc_count += 1
                    if role.name == "level":
                        level_count += 1
                    if role.name == "country":
                        country_count += 1
                    if role.name == "profile":
                        profile_count += 1

        values = [f'Members: {member_count}',
                  f'Members Role: {member_role_count}',
                  f'Members on Team Instinct: {instinct_count}',
                  f'Members on Team Mystic: {mystic_count}',
                  f'Members on Team Valor: {valor_count}',
                  f'Members with IGN set: {ign_count}',
                  f'Members with TC set: {tc_count}',
                  f'Members with level set: {level_count}',
                  f'Members with country set: {country_count}',
                  f'Members with completed Nexus Profiles: {profile_count}']

        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.add_field(name='Server Stats:', value='\n'.join(values), inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))

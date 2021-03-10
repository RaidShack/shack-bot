import discord
import sys
from discord.ext import commands
from subprocess import run, STDOUT


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def api(self, ctx, action):
        if action == 'up':
            self.bot.load_extension('cogs.routes')
        if action == 'down':
            self.bot.unload_extension('cogs.routes')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def kill(self, ctx):
        await ctx.bot.logout()
        print('shack-bot killed')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, modules: str):
        for module in self.bot.initial_extensions if modules == 'all' else [modules]:
            try:
                self.bot.load_extension(module)
            except Exception as e:
                await ctx.send(e)
            else:
                await ctx.send(f'{module} loaded')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, modules: str):
        for module in self.bot.initial_extensions if modules == 'all' else [modules]:
            try:
                self.bot.unload_extension(module)
            except Exception as e:
                await ctx.send(e)
            else:
                await ctx.send(f'{module} unloaded')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, modules: str):
        for module in self.bot.initial_extensions if modules == 'all' else [modules]:
            try:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
            except Exception as e:
                await ctx.send(e)
            else:
                await ctx.send(f'{module} reloaded')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pull(self, ctx):
        git_log = open('git.log', 'w')
        pip_log = open('pip.log', 'w')
        run(['git', 'pull'], stdout=git_log, stderr=STDOUT, text=True)
        run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], stdout=pip_log, stderr=STDOUT, text=True)
        files = [
            discord.File('git.log'),
            discord.File('pip.log'),
        ]
        return await ctx.send('git pull done', files=files)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logs(self, ctx, delete=None):
        logs = ['git.log', 'pip.log', 'access.log', 'error.log']
        files = []
        if delete:
            for log in logs:
                open(log, 'w').close()
            await ctx.send('logs deleted')
        else:
            for log in logs:
                files.append(discord.File(log))
            await ctx.send('current logs', files=files)


def setup(bot):
    bot.add_cog(Admin(bot))

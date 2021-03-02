import asyncio
import config
import io
import re
from discord.ext import commands
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class Gdrive(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_doc(filename):
        service = build('drive', 'v3', developerKey=config.gdrive_api)
        param = {"q": "'" + config.gdrive_folder + "' in parents"}
        result = service.files().list(**param).execute()
        files = result.get('files')
        file = next((item for item in files if item['name'] == filename), None)
        if not file:
            return None
        request = service.files().export(fileId=file['id'], mimeType='text/plain')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            done = downloader.next_chunk()
        fh.seek(0)
        wrapper = io.TextIOWrapper(fh, encoding='utf-8-sig')
        return re.sub(r'\n\s*\n', '\n\n', wrapper.read())

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def pin(self, ctx, filename):

        def not_pinned(check):
            return not check.pinned

        async with ctx.typing():
            doc = self.get_doc(filename)
        if doc:
            message = await ctx.send(doc)
            await message.pin()
            await ctx.channel.purge(limit=100, check=not_pinned)
        else:
            await ctx.send('Document not found')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def post(self, ctx, filename):
        async with ctx.typing():
            doc = self.get_doc(filename)
        if doc:
            await ctx.send(doc)
            await ctx.message.delete()
        else:
            await ctx.send('Document not found')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def preview(self, ctx, filename):
        async with ctx.typing():
            doc = self.get_doc(filename)
        if doc:
            message = await ctx.send(doc)
            await asyncio.sleep(30)
            await message.delete()
            await ctx.message.delete()
        else:
            await ctx.send('Document not found')

    @pin.error
    @post.error
    @preview.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, you can't run this command")
        else:
            raise error


def setup(bot):
    bot.add_cog(Gdrive(bot))

import asyncio
import os
import urllib.request
import discord

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

    @staticmethod
    async def do_attachment(ctx, message):
        if '[img]' in message:
            content = message.split('[img]')
            content_url = content[0] if '[img]' in content[0] else content[1]
            content_text = '' if '[img]' in content[0] else content[0]
            url = content_url.replace('[img]', '')
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = io.BytesIO(urllib.request.urlopen(req).read())
            return await ctx.send(content_text, file=discord.File(data, os.path.split(url)[-1]))
        else:
            return await ctx.send(message)

    async def do_message(self, ctx, doc, action=None, delay=None):
        to_delete = []
        if '[break]' in doc:
            messages = doc.split('[break]\n')
            for message in messages:
                message = await self.do_attachment(ctx, message)
                if action == 'pin':
                    await message.pin()
                elif action == 'preview':
                    to_delete.append(message.id)
            if to_delete:
                await asyncio.sleep(delay)
                for message_id in to_delete:
                    message = await ctx.fetch_message(message_id)
                    await message.delete()
        else:
            message = await self.do_attachment(ctx, doc)
            if action == 'pin':
                await message.pin()
            elif action == 'preview':
                await asyncio.sleep(delay)
                await message.delete()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def pin(self, ctx, filename):

        def not_pinned(check):
            return not check.pinned

        async with ctx.typing():
            doc = self.get_doc(filename)
        if doc:
            await self.do_message(ctx, doc, 'pin')
            await ctx.channel.purge(limit=100, check=not_pinned)
        else:
            await ctx.send('Document not found')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def post(self, ctx, filename):
        async with ctx.typing():
            doc = self.get_doc(filename)
        if doc:
            await self.do_message(ctx, doc)
            await ctx.message.delete()
        else:
            await ctx.send('Document not found')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def preview(self, ctx, filename, delay=30):
        async with ctx.typing():
            doc = self.get_doc(filename)
        if doc:
            await self.do_message(ctx, doc, 'preview', delay)
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

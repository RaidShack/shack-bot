import re

from discord.ext import commands
import pickle
import os
import io

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload


class Post(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.scopes = ['https://www.googleapis.com/auth/drive.metadata',
                       'https://www.googleapis.com/auth/drive',
                       'https://www.googleapis.com/auth/drive.file'
                       ]

    def get_gdrive_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # initiate Google Drive service API
        return build('drive', 'v3', credentials=creds)

    @commands.command()
    async def post(self, ctx, filename):
        async with ctx.typing():
            file_id = ""
            message = ""
            service = self.get_gdrive_service()
            results = service.files().list(fields="files(id, name, parents)").execute()
            items = results.get('files', [])
            if not items:
                message = 'No file found.'
            else:
                for item in items:
                    if item['name'] == filename and self.bot.gdrive in item['parents']:
                        file_id = item['id']
            request = service.files().export(fileId=file_id, mimeType='text/plain')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                done = downloader.next_chunk()
            fh.seek(0)
            wrapper = io.TextIOWrapper(fh, encoding='utf-8-sig')
        themessage = await ctx.send(re.sub(r'\n\s*\n', '\n\n', wrapper.read()))
        await themessage.pin()


def setup(bot):
    bot.add_cog(Post(bot))

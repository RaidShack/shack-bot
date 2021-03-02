from discord.ext import commands
from quart import Quart, request, send_from_directory
from quart_cors import cors
import config
import discord

app = Quart(__name__)
app = cors(app, allow_origin="*")


class Routs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @app.route("/.well-known/acme-challenge/<challenge>")
    async def acme_challenge(challenge):
        return await send_from_directory('.well-known/acme-challenge', challenge)

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    async def index():
        data = await request.get_json()
        print(data)
        return 'OK', 200


def setup(bot):
    bot.loop.create_task(app.run_task(certfile=config.cert, keyfile=config.key if config.cert else None))
    bot.add_cog(Routs(bot))

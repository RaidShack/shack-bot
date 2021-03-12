from discord.ext import tasks, commands
from quart import Quart, request, send_from_directory
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart_cors import route_cors
from config import bind, certfile, keyfile, loglevel
import discord


class Routes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api.start()

    quart = Quart(__name__)

    def cog_unload(self):
        self.api.cancel()

    @tasks.loop()
    async def api(self):
        options = {'bind': bind,
                   'certfile': certfile,
                   'keyfile': keyfile,
                   'loglevel': loglevel,
                   'accesslog': 'access.log',
                   'errorlog': 'error.log',
                   }
        await serve(self.quart, Config.from_mapping(options))

    @staticmethod
    @quart.route('/.well-known/acme-challenge/<challenge>')
    async def acme_challenge(challenge):
        return await send_from_directory('.well-known/acme-challenge', challenge)

    @staticmethod
    @quart.route('/', methods=['GET', 'POST'])
    @route_cors(allow_origin='*')
    async def index():
        data = await request.get_json()
        return 'OK', 200

    @staticmethod
    @quart.route('topgg/', methods=['POST'])
    @route_cors(allow_origin='*')
    async def topgg():
        data = await request.get_json()
        print(data)
        return 'OK', 200


def setup(bot):
    bot.add_cog(Routes(bot))

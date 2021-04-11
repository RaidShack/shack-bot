import random
import ssl
from discord.ext import tasks, commands
from quart import Quart, request, send_from_directory
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart_cors import route_cors
from config import bind, certfile, keyfile, loglevel
import discord

quart = Quart(__name__)


class Routes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api.start()

        @quart.route('/.well-known/acme-challenge/<challenge>')
        async def acme_challenge(challenge):
            return await send_from_directory('.well-known/acme-challenge', challenge)

        @quart.route('/', methods=['GET', 'POST'])
        @route_cors(allow_origin='*')
        async def index():
            return 'OK', 200

        @quart.route('/topgg', methods=['POST'])
        @route_cors(allow_origin='*')
        async def topgg():
            party_hat = [
                'https://img.pokemondb.net/sprites/go/normal/pikachu-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/raichu-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/raticate-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/wobbuffet-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/wurmple-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/pichu-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/pikachu-red-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/squirtle-red-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/bulbasaur-red-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/charmander-red-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/eevee-red-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/nidorino-red-party-hat.png',
                'https://img.pokemondb.net/sprites/go/normal/gengar-red-party-hat.png',
            ]
            data = await request.get_json()
            guild = self.bot.get_guild(int(data['guild']))
            channel = guild.get_channel(820730247682850826)
            embed = discord.Embed(title='Thanks for the vote over at top.gg,\nwe appreciate the support!',
                                  description=f'[Show your :two_hearts: and vote for the {guild.name}!](https://top.gg/servers/736436788696055829)',
                                  color=discord.Color.random())
            embed.set_author(name='top.gg Servers', url='https://top.gg/servers/736436788696055829',
                             icon_url='https://static.raidshack.com/topgg/serverbot.png')
            embed.set_thumbnail(url=random.choice(party_hat))
            if data['type'] == 'upvote':
                await channel.send(f'<@{data["user"]}>, you\'re awesome!\n\n', embed=embed)
            return 'OK', 200

    def cog_unload(self):
        self.api.cancel()

    @tasks.loop()
    async def api(self):
        options = {'certfile': certfile,
                   'keyfile': keyfile,
                   'bind': '127.0.0.1:5000',
                   'insecure-bind': '127.0.0.1:8000',
                   'loglevel': loglevel,
                   'accesslog': 'access.log',
                   'errorlog': 'error.log',
                   }
        await serve(quart, Config.from_mapping(options))
        self.bot.loop.set_exception_handler(self._exception_handler)

    @staticmethod
    def _exception_handler(loop, context):
        exception = context.get("exception")
        if isinstance(exception, ssl.SSLError):
            pass
        else:
            loop.default_exception_handler(context)


def setup(bot):
    bot.add_cog(Routes(bot))

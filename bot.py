import os
from twitchio.ext import commands
from tinydb import TinyDB
from utils import add_og, get_ogs, if_og, update_last_so
from dotenv import load_dotenv

load_dotenv()

cogs = [
    'cogs.og'
]


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=os.getenv('ACCESS_TOKEN'), prefix='!', initial_channels=['psuedoo'])
        self.db = TinyDB('db.json')

        for cog in cogs:
            self.load_module(cog)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        print(f"{message.channel.name} | {message.author.name}:{message.content}")

        if message.content.startswith('!'):
            await self.handle_commands(message)
        else:
            await self.shoutout(message)
            

    @if_og
    async def shoutout(self, message):
        update_last_so(message.author)
        await message.channel.send(f'!so {message.author.name}')

bot = Bot()
bot.run()
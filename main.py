import os
from twitchio.ext import commands
from tinydb import TinyDB
from utils import add_og, get_ogs, if_og, update_last_so
from dotenv import load_dotenv

load_dotenv()


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.getenv('ACCESS_TOKEN'), prefix='!', initial_channels=['psuedoo'])
        self.db = TinyDB('db.json')

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)

        if message.content.startswith('!'):
            await self.handle_commands(message)
        else:
            await self.shoutout(message)
            

    @if_og
    async def shoutout(self, message):
        update_last_so(message.author)
        await message.channel.send(f'!so {message.author.name}')

    @commands.command()
    async def add_og(self, ctx: commands.Context, user):
        username = user.strip('@')
        users = await self.fetch_users([username])

        if not users[0] == username:
            await ctx.send(f'User {username} not found')
            return

        user = users[0]
        ogs = self.db.table('ogs')
        added = add_og(ctx, user)
        

        if not added:
            await ctx.send(f'{user.name} is already an Oh Gee')
            return

        await ctx.send(f'Added {user.name} to the list of Oh Gees')

    @commands.command()
    async def get_ogs(self, ctx: commands.Context):
        ogs = get_ogs()
        await ctx.send(f'Oh Gees: {ogs}')

bot = Bot()
bot.run()
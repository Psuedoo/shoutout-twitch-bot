import os
from twitchio.ext import commands
from tinydb import TinyDB, Query
from dotenv import load_dotenv
from checks import if_og, mod_only
from utils import update_last_so

load_dotenv()

cogs = ["cogs.og", "cogs.admin"]


class Bot(commands.Bot):
    def __init__(self):
        self.db = TinyDB("db.json")

        self.initial_channels = self.get_initial_channels()

        print(f"Initial channels: {self.initial_channels}")

        super().__init__(
            token=os.getenv("ACCESS_TOKEN"),
            prefix="!",
            initial_channels=self.initial_channels,
        )

        for cog in cogs:
            self.load_module(cog)

    def initialize_channels(self):
        table = self.db.table("initial_channels")
        Channel = Query()

        # Channels to always add to db if not present
        initial_channels = ["psuedoo"]
        for channel in initial_channels:
            if not table.contains(Channel.name == channel):
                table.insert({"name": channel})

    def get_initial_channels(self):
        self.initialize_channels()
        return [channel["name"] for channel in self.db.table("initial_channels")]

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        if message.echo:
            return

        print(f"{message.channel.name} | {message.author.name}:{message.content}")

        if message.content.startswith("!"):
            await self.handle_commands(message)
        else:
            await self.shoutout(message)

    @if_og
    async def shoutout(self, message):
        update_last_so(message.channel.name, message.author)
        await message.channel.send(f"!so {message.author.name}")


bot = Bot()
bot.run()

from twitchio.ext import commands
from utils import add_channel
from checks import mod_only


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(name="joinchannel")
    @mod_only
    def add_channel(self, ctx, channel):
        channel = channel.strip("@")
        add_channel(channel)
        self.bot.join_channels([channel])
        ctx.send(f"Joined channel {channel}")


def prepare(bot):
    bot.add_cog(AdminCog(bot))

from twitchio.ext import commands
from utils import add_og, get_ogs, update_last_so
from checks import mod_only


class OGCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(name="addog")
    @mod_only
    async def add_og_cmd(self, ctx: commands.Context, user: str):
        username = user.strip("@")
        users = await self.bot.fetch_users([username])

        if not users[0].name == username:
            await ctx.send(f"User {username} not found")
            return

        user = users[0]
        ogs = self.db.table("ogs")
        added = add_og(ctx, user)

        if not added:
            await ctx.send(f"{user.name} is already an Oh Gee")
            return

        await ctx.send(f"Added {user.name} to the list of Oh Gees")

    @commands.command(name="getogs")
    @mod_only
    async def get_ogs_cmd(self, ctx: commands.Context):
        ogs = get_ogs(channel=ctx.channel.name)
        await ctx.send(f"Oh Gees: {ogs}")


def prepare(bot):
    bot.add_cog(OGCog(bot))

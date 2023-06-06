from twitchio.ext import commands
from utils import mod_only


class OGCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db


    @commands.command()
    @mod_only
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
    @mod_only
    async def get_ogs(self, ctx: commands.Context):
        ogs = get_ogs()
        await ctx.send(f'Oh Gees: {ogs}')

def prepare(bot):
    bot.add_cog(OGCog(bot))
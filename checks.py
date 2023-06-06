import datetime
from utils import get_og, update_last_so, add_og


def mod_only(func):
    async def wrapper(self, ctx, *args, **kwargs):
        if ctx.author.is_mod:
            await func(self, ctx, *args, **kwargs)

    return wrapper


def if_og(func):
    async def inner(self, message):
        now = datetime.datetime.now()

        og = get_og(channel=message.channel.name, name=message.author.name)
        # TODO: Add a cooldown for ogs
        if og:
            last_so = og.get("last_so", now)
            if not last_so:
                last_so = now
                await func(self, message)
            if last_so < now - datetime.timedelta(hours=1):
                update_last_so(channel=message.channel.name, user=message.author)
                await func(self, message)
            else:
                await message.channel.send(
                    f"{message.author.name} has already been shouted out in the last hour"
                )
                return
        elif message.author.is_mod or message.author.is_vip:
            add_og(message, message.author)
            await func(self, message)

    return inner

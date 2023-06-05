import datetime
from tinydb import TinyDB, Query

def if_og(func):
    async def wrapper(self, message):
        now = datetime.datetime.now()

        og = get_og(message.author.name)
        # TODO: Add a cooldown for ogs
        if og:
            last_so = og.get('last_so', now)
            if not last_so:
                last_so = now
                await func(self, message)
            if last_so < now - datetime.timedelta(hours=1):
                last_so = update_last_so(message.author)
                await func(self, message)
            else:
                await message.channel.send(f'{message.author.name} has already been shouted out in the last hour')
                return 
        elif message.author.is_mod or message.author.is_vip:
            add_og(message, message.author)
            await func(self, message)
    return wrapper

def add_og(ctx, user):
    db = TinyDB('db.json')
    ogs = db.table('ogs')
    if ogs.search(Query().id == user.id):
        return False
    
    ogs.insert({'name': user.name, 'id': user.id, 'last_so': None, 'added_by': ctx.author.name})
    return True

def get_ogs():
    db = TinyDB('db.json')
    ogs = db.table('ogs')
    return [og['name'].lower() for og in ogs.all()]

def get_og(name: str):
    db = TinyDB('db.json')
    ogs = db.table('ogs')
    og = ogs.search(Query().name == name)
    return og[0] if og else None

def update_last_so(user):
    db = TinyDB('db.json')
    ogs = db.table('ogs')
    ogs.update({'last_so': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Query().id == user.id)
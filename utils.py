import datetime
from tinydb import TinyDB, Query


def add_og(ctx, user):
    db = TinyDB("db.json")
    ogs = db.table("ogs")
    if ogs.search(Query().fragment({'id': user.id, 'channel': ctx.channel.name})):
        return False

    ogs.insert(
        {
            "name": user.name,
            "id": user.id,
            "last_so": None,
            "added_by": ctx.author.name,
            "channel": ctx.channel.name,
        }
    )
    return True


def get_ogs(channel: str):
    db = TinyDB("db.json")
    ogs_table = db.table("ogs")
    ogs = ogs_table.search(Query().channel == channel)
    return [og["name"].lower() for og in ogs]


def get_og(channel: str, name: str):
    db = TinyDB("db.json")
    ogs = db.table("ogs")
    og = ogs.search(Query().name == name, Query().channel == channel)
    return og[0] if og else None


def update_last_so(channel: str, user):
    db = TinyDB("db.json")
    ogs_table = db.table("ogs")
    ogs = ogs_table.search(Query().name == user.name, Query().channel == channel)
    ogs.update(
        {"last_so": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        Query().id == user.id,
    )


def add_channel(channel):
    db = TinyDB("db.json")
    table = db.table("initial_channels")
    Channel = Query()
    if not table.contains(Channel.name == channel):
        table.insert({"name": channel})

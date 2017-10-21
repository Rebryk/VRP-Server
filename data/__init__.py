import ujson as json

from pony import orm

db = orm.Database()

from .audio import Audio
from .user import User

with open("config/db.json") as f:
    config = json.load(f)

    db.bind(provider="postgres",
            user=config["user"],
            password=config["password"],
            host=config["host"],
            database=config["database"])

    db.generate_mapping(create_tables=True)

__all__ = ("Audio", "User")

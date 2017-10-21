from . import db
from pony import orm
from uuid import UUID


class User(db.Entity):
    id = orm.PrimaryKey(int, auto=False)
    uuid = orm.Required(UUID, unique=True)

    audio = orm.Set("Audio")

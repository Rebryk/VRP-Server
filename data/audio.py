from . import db
from pony import orm
from datetime import datetime


class Audio(db.Entity):
    date = orm.Required(datetime, default=lambda: datetime.now())
    user = orm.Optional("User")
    url = orm.PrimaryKey(str, auto=False)
    text = orm.Optional(str)

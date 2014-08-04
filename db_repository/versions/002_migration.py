from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Users = Table('Users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=50)),
    Column('fullname', String(length=100)),
    Column('email', String(length=120)),
    Column('password', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(2)),
    Column('status', SmallInteger, default=ColumnDefault(1)),
    Column('activation_code', String(length=12)),
    Column('about_me', String(length=200)),
    Column('last_seen', DateTime),
    Column('badges', String(length=100)),
    Column('sosachdang', SmallInteger, default=ColumnDefault(0)),
    Column('sosachdaban', SmallInteger, default=ColumnDefault(0)),
    Column('sosachdamua', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Users'].columns['badges'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Users'].columns['badges'].drop()

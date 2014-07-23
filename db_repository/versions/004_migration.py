from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
book = Table('book', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('tensach', VARCHAR(length=100)),
    Column('tacgia', VARCHAR(length=100)),
    Column('truong', VARCHAR(length=100)),
    Column('chuyennganh', VARCHAR(length=100)),
    Column('giaovien', VARCHAR(length=100)),
    Column('giaban', SMALLINT),
    Column('tinhtrang', VARCHAR(length=100)),
    Column('thoigiandang', DATETIME),
    Column('noigapmat', VARCHAR(length=300)),
    Column('thoigiangapmat', VARCHAR(length=200)),
    Column('lienhe', VARCHAR(length=200)),
    Column('user_id', INTEGER),
)

users_user = Table('users_user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=50)),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('status', SMALLINT),
    Column('activation_code', VARCHAR(length=12)),
)

Books = Table('Books', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tensach', String(length=100)),
    Column('tacgia', String(length=100)),
    Column('truong', String(length=100)),
    Column('chuyennganh', String(length=100)),
    Column('giaovien', String(length=100)),
    Column('giaban', SmallInteger, default=ColumnDefault(0)),
    Column('tinhtrang', String(length=100)),
    Column('thoigiandang', DateTime),
    Column('noigapmat', String(length=300)),
    Column('thoigiangapmat', String(length=200)),
    Column('lienhe', String(length=200)),
    Column('user_id', Integer),
)

Users = Table('Users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('email', String(length=120)),
    Column('password', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(2)),
    Column('status', SmallInteger, default=ColumnDefault(1)),
    Column('activation_code', String(length=12)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['book'].drop()
    pre_meta.tables['users_user'].drop()
    post_meta.tables['Books'].create()
    post_meta.tables['Users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['book'].create()
    pre_meta.tables['users_user'].create()
    post_meta.tables['Books'].drop()
    post_meta.tables['Users'].drop()

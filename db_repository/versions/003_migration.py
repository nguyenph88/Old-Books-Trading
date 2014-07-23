from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
book = Table('book', post_meta,
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].drop()

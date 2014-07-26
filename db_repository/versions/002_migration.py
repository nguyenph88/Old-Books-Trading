from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Books = Table('Books', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('truong', String(length=100)),
    Column('khuvuc', String(length=100)),
    Column('chuyennganh', String(length=100)),
    Column('giaovien', String(length=100)),
    Column('tensach', String(length=100)),
    Column('tacgia', String(length=100)),
    Column('theloai', String(length=100)),
    Column('tinhtrang', String(length=100)),
    Column('giaban', SmallInteger, default=ColumnDefault(0)),
    Column('noigapmat', String(length=300)),
    Column('thoigiangapmat', String(length=200)),
    Column('lienhe', String(length=200)),
    Column('image', String(length=200)),
    Column('thoigiandang', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Books'].columns['image'].create()
    post_meta.tables['Books'].columns['theloai'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Books'].columns['image'].drop()
    post_meta.tables['Books'].columns['theloai'].drop()

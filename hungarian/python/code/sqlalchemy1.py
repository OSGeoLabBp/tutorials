from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, PrimaryKeyConstraint
from sqlalchemy import String, DateTime, Float
from sqlalchemy.sql import select
import datetime

metadata = MetaData()
engine = create_engine('postgresql:///siki', echo=True)
conn = engine.connect()
pdata = Table('pdata', metadata,
    Column('id', String(20)),
    Column('easting', Float),
    Column('northing', Float),
    Column('elev', Float),
    Column('d', DateTime),
    PrimaryKeyConstraint('id', 'd'))
metadata.create_all(engine)
s = select([pdata])
result = conn.execute(s)

for row in result:
    print row

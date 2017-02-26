from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select

metadata = MetaData()
engine = create_engine('postgresql:///siki', echo=True)
conn = engine.connect()
pdata = Table('pdata', metadata, autoload=True, autoload_with=engine)

s = select([pdata])
result = conn.execute(s)

for row in result:
    print row

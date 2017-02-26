from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, PrimaryKeyConstraint
from sqlalchemy import String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
metadata = MetaData()
engine = create_engine('postgresql:///siki', echo=False)

class pdata(Base):
    __table__ = Table('pdata', Base.metadata, autoload=True,
        autoload_with=engine)

session = sessionmaker()
session.configure(bind=engine)

# session and ORM
s = session()
rec = pdata(id='3', easting=-1.012, northing=3.153, d=datetime.datetime.now())
s.add(rec)
s.commit()
print s.query(pdata).count()
for row in s.query(pdata).filter(pdata.id.in_(['1', '2'])).order_by(pdata.id).all():
    print "%s, %.3f %.3f, %s" % (row.id, row.easting, row.northing, row.d.strftime('%Y-%m-%d %H:%m'))
s.close()

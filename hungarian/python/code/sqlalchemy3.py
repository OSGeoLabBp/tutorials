#!/usr/bin/env python
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
# html 
print ("""<!DOCTYPE html>
<html>
    <header>
    <title>Python postgres table to  html</title>
    </header>
    <body>
    <table>
""")
for row in s.query(pdata).filter(pdata.id.in_(['1', '2'])).order_by(pdata.id).all():
    print ("<tr><td>%s</td><td>%.3f</td><td>%.3f</td><td>%s</td></tr>" % (row.id, row.easting, row.northing, row.d.strftime('%Y-%m-%d %H:%m')))
print ("""</table>
    </body>
    </html>
""")
s.close()

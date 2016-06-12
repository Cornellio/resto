#!/usr/bin/env python

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Restaurant, Base, MenuItem
import datetime
import random

engine = create_engine('sqlite:///restaurants.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

session = DBSession()

def query1():
    r = session.query(Restaurant).order_by(Restaurant.id.asc()).all()

    for item in r:
        print item.id
        print item.name

def query2():
# r = session.query(User).filter_by(name='ed').all()
    r = session.query(Restaurant).filter_by(id='4')

    for x in r:
        print x.id
        print x.name

def query3():
    # session.query(Restaurant).filter(Restaurant.id==23).delete()
    u = Restaurant(name = "qAdd 1")
    session.add(u)
    session.commit()



## Try to find by name
# x = 'parley'
# print type(restos_all_l)
# if x in restos_all_l:
#     print 'found'
# else
#     print 'not'

if __name__ == '__main__':
    query3()
    query1()

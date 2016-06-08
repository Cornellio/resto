#!/usr/bin/env python

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Shelter, Base, Puppy
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

# shelters = session.query(Shelter).all()
puppys = session.query(Puppy).all()

puppy_list = []
for puppy in puppys:
  puppy_list.append(puppy.name)

# All puppies sorted
def query_one():
  for puppy in sorted(puppy_list):
    print puppy
  # Same but with sql orm instead
  result = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
  for item in result:
    print item[0]

# All puppies < 6 mos old

def query_two():
  today = datetime.date.today()
  result = session.query(Puppy.name, Puppy.dateOfBirth).order_by(Puppy.dateOfBirth.desc()).all()
  for item in result:
    puppy_months = diff_month(today, item[1])
    print item, puppy_months
    if puppy_months < 6:
      print "{name}: {months}".format(name=item[0], months=puppy_months)

def query_three():
  result = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()

  for item in result:
    print item[0], item[1]

def query_four():
  result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
  for item in result:
    print item[0].id, item[0].name, item[1]


def diff_month(d1, d2):
  delta = d1 - d2
  return delta.days / 30


if __name__ == '__main__':
  # query_one()
  query_two()
  # query_three()
  query_four()

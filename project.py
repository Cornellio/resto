#!/usr/bin/env python

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Restaurant, MenuItem, Base
from flask import Flask

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def helloworld():
    return 'Hello World'


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 80)

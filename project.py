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
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

    # output = items.name
    output = ''
    for item in items:
        output += item.name
        output += '</br>'
        output += item.price
        output += '</br>'
        output += item.description
        output += '</br></br>'

    return output


@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return 'task 1. create new menu item'


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return 'task 2. edit a menu item'


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return 'task 3. delete a menu item'



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)

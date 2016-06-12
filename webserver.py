#!/usr/bin/env python

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Restaurant, MenuItem, Base
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import datetime
import cgi


def DBSession():
    engine = create_engine('sqlite:///restaurants.db')
    Base.metadata.bind = engine
    session = sessionmaker(bind=engine)
    return session()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # list all restaurants
            if self.path.endswith("/restaurants") or self.path.endswith("/restos"):
                session = DBSession()
                result = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                # Write html headers
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Restaurants</h2>"
                output += "<ul>"
                for restaurant in result:
                    link_edit = ' - <a href="/restaurants/%s/edit">edit</a>' % (str(restaurant.id))
                    link_del = '<a href="/restaurants/%s/delete"> | delete</a>' % (str(restaurant.id))
                    output += "<li>" + restaurant.name + link_edit + link_del + "</li>\n"
                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output

            # Add new restaurant
            if self.path.endswith("/restaurants/new"):
                # create new resto
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''
                    <form method='POST' enctype='multipart/form-data'
                    action='http://localhost:8080/'><h2>Add New Restaurant:</h2><input name="create_new" type="text"><input type="submit" value="Submit"> </form>
                    '''
                output += "</body></html>"
                self.wfile.write(output)
                return

            # Edit a restaurant with given id
            if self.path.endswith("/edit"):
                session = DBSession()

                # Slice the id from URI
                restaurant_id = self.path.split('/')[2]
                match = session.query(Restaurant).filter_by(id = restaurant_id)
                for restaurant in match:
                    restaurant = restaurant.name

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<h1> Rename Restaurant</h1>'
                output += '<form method="POST" enctype="multipart/form-data"'
                output += 'action="http://localhost:8080/"><h2>Change %s to </h2>' % (restaurant)
                output += '<input name="new_name" type="text">'
                output += '<input name="restaurant_id" type="hidden" value="%s">' % (restaurant_id)
                output += '<input type="submit" value="Go for it"> </form>'
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)

                # Hello world test
                if fields.get('message'):
                    messagecontent = fields.get('message')
                    output = ""
                    output +=  "<html><body>"
                    output += " <h2> Okay, how about this: </h2>"

                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                    output += "</html></body>"

                    self.wfile.write(output)
                    print output

                # Add restaurant
                if fields.get('create_new'):
                    session = DBSession()
                    restaurante_name = fields.get('create_new')
                    new_restaurant = Restaurant(name = restaurante_name[0])
                    session.add(new_restaurant)
                    session.commit()
                    print "DB: inserting new restaurant: %s" % new_restaurant

                    # Redirect back to restaurant list
                    # self.send_response(301)
                    # self.send_header('Content-type', 'text/html')
                    # self.send_header('Location', 'http://localhost:8080/restaurants')
                    # self.end_headers()

                    # Verify new resto got put in DB
                    # result = session.query(Restaurant.name[new_restaurant])
                    # print result

                    # self.wfile.write(output)
                    # print output

                # Edit restaurant
                if fields.get('new_name'):
                    print 'Start edit:',
                    print 'Got POST fields: ', fields
                    id_current = fields.get('restaurant_id')
                    name_new = fields.get('new_name')
                    print id_current
                    print name_new

                    session = DBSession()

                    print '# Remove existing entry and add new'
                    session.query(Restaurant).filter(Restaurant.id==id_current[0]).delete()
                    new = Restaurant(name = name_new[0])
                    session.add(new)
                    session.commit()


        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()

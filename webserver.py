#!/usr/bin/env python

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Restaurant, MenuItem, Base
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import datetime
import cgi


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # list all restos
            if self.path.endswith("/restaurants") or self.path.endswith("/restos"):
                engine = create_engine('sqlite:///restaurants.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                result = session.query(Restaurant.name).order_by(Restaurant.name.asc()).all()
                # Write html headers
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Restaurants</h2>"
                output += "<ul>"
                for item in result:
                    link_edit = ' - <a href="http://localhost:8080/restaurants">edit</a>'
                    link_del = '<a href="http://localhost:8080/restaurants"> | delete</a>'
                    output += "<li>" + item[0] + link_edit + link_del + "</li>\n"
                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output


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

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""

            output +=  "<html><body>"
            output += " <h2> Okay, how about this: </h2>"

            output += "<h1> %s </h1>" % messagecontent[0]

            output += '''<form method='POST' enctype='multipart/form-data' action='http://localhost:8080/'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''

            output += "</html></body>"

            self.wfile.write(output)
            print output

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

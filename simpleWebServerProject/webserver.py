from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


# set the DB connection
engine = create_engine(
    'sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantId).one()
                if restaurantQuery != []:
                    # send response as success
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    # build output HTML content
                    output = ""
                    output += "<html><body>"
                    output += "<h3>Are you sure you want to delete <b>%s</b> ?</h3><br><br>" %restaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" %restaurantId
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantId).one()
                if restaurantQuery != []:
                    # send response as success
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    # build output HTML content
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += restaurantQuery.name
                    output += "</h1></br></br>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" %restaurantId
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" %restaurantQuery.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                # send response as success
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # build output HTML content
                output = ""
                output += "<html><body>"
                output += "<h1>Add a new restaurant:</h1></br></br>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='addRestaurantName' type='text' placeholder='Eg. Royal Taj'>"
                output += "<input type='submit' value='Add'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                # send response as success
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # build output HTML content
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add a new restaurant here</a></br></br>"
                output += "<h1>Restaurants List:</h1>"

                # get the data
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<div>"
                    output += restaurant.name + "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a></br>" %restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a></br>" %restaurant.id
                    output += "</div></br></br>"

                output += "</body></html>"

                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File not Found %s"%self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantId).one()

                if restaurantQuery != []:
                    # delete the object
                    session.delete(restaurantQuery)
                    session.commit()

                    # send response as success
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # redirect output to /restaurants
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantId).one()

                if restaurantQuery != []:
                    # set the new name
                    restaurantQuery.name = messagecontent[0]
                    session.add(restaurantQuery)
                    session.commit()

                    # send response as success
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # redirect output to /restaurants
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return

            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('addRestaurantName')

                # add an entry into 'Restaurant' table
                print "Messagecontent[0]="+messagecontent[0]
                restaurantObj = Restaurant(name = messagecontent[0])
                session.add(restaurantObj)
                session.commit()

                # send response as success
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                # redirect output to /restaurants
                self.send_header('Location', '/restaurants')
                self.end_headers()

            return
        except IOError:
            self.send_error(404, "File not Found %s"%self.path)
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" %port
        server.serve_forever()

    except KeyboardInterrupt:
        print "Stoping the web server..."
        server.socket.close()


if __name__ == '__main__':
    main()

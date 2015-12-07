#/usr/bin/python
# import modules
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time, socket, urllib2

# set up variables
PORT_NUMBER = 80
timeStr = time.strftime("%c") # obtains current time
hostName = socket.gethostname()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = response.read()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
privateIp = response.read()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-ipv4')
publicIp = response.read()

# compose html
htmlFormat = """
<html>
  <Title>Service Discovery Demo</Title>
<body>
  <p>The host name or container id is:  {hostName}</p>
  <p>The EC2 instance ID is:  {instance_id}</p>
  <p>The instance public IP is:  {publicIp}</p>
  <p>The instance private IP is:  {privateIp}</p>
  <p>The time (UTC) this server started is:  {timeStr}</p>
</body>
</html> """

composed_html = htmlFormat.format(**locals())

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(composed_html)
        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()


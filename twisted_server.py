#/usr/bin/python
# import modules
import time, socket, urllib2
from twisted.web import server, resource
from twisted.internet import reactor

# set up static variables
# PORT_NUMBER = 80 # not needed here - using 8080 instead
hostName = socket.gethostname()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = response.read()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
privateIp = response.read()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-ipv4')
publicIp = response.read()
timeStr = time.strftime("%c") # obtains current time at server launch

# compose html
htmlFormat = """
<html>
  <Title>Service Discovery Demo</Title>
<body>
  <p>The host name or container id is:  {hostName}</p>
  <p>The EC2 instance ID is:  {instance_id}</p>
  <p>The instance public IP is:  {publicIp}</p>
  <p>The instance private IP is:  {privateIp}</p>
  <p>The time (UTC) this content was served is:  {timeStr}</p>
</body>
</html> """

composed_html = htmlFormat.format(**locals())

#This class will handles any incoming request from the browser 
class SimpleServer(resource.Resource):
  isLeaf = True
  def render_GET(self, request):
    timeStr = time.strftime("%c") # obtains current time of get
    composed_html = htmlFormat.format(hostName = hostName, instance_id = instance_id, publicIp = publicIp, privateIp = privateIp, timeStr = timeStr) # refresh the html, locals doesn't seem to work here (different scope? - investigate later)
    print request
    return composed_html

site = server.Site(SimpleServer())
reactor.listenTCP(8080, site)
reactor.run()
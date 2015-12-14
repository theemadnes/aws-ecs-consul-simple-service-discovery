#/usr/bin/python
# import modules
import time, socket, urllib2
from twisted.web import server, resource
from twisted.internet import reactor
import json

# set up static variables
serviceName = 'py-basic-web-server' # change this if your service name is something else
hostName = socket.gethostname()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = response.read()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
privateIp = response.read()
response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-ipv4')
publicIp = response.read()

# create the string that will be used to reflect the container IPs
addressList = ''

# set up the html doc that will be used to render data
htmlFormat = """
<html>
  <Title>Service Discovery Demo</Title>
<body>
  <p>The host name or container id is:  {hostName}</p>
  <p>The EC2 instance ID is:  {instance_id}</p>
  <p>The instance public IP is:  {publicIp}</p>
  <p>The instance private IP is:  {privateIp}</p>
  <p>The time (UTC) this content was served is:  {timeStr}</p>
  <p>*****************************************************</p>
  <p>The current container instance(s) supporting this service is / are:  {addressList}</p>

</body>
</html> """

# composed_html = htmlFormat.format(**locals())

#This class will handles any incoming request from the browser 
class SimpleServer(resource.Resource):
  isLeaf = True
  def render_GET(self, request):
    addressList = '' # reset the ip string
    timeStr = time.strftime("%c") # obtains current time of GET from client

    try:

      # get service information from consul
      response = urllib2.urlopen('http://' + privateIp + ':8500/v1/catalog/service/' + serviceName)
      rawJson = response.read()
      parsedJson = json.loads(rawJson)

      for item in parsedJson:

        addressList = addressList + item['Address'] + ' '

    except:

      addressList = ''

    composed_html = htmlFormat.format(hostName = hostName, instance_id = instance_id, publicIp = publicIp, privateIp = privateIp, timeStr = timeStr, addressList = addressList) # refresh the html, locals doesn't seem to work here (different scope? - investigate later)
    print request
    return composed_html

site = server.Site(SimpleServer())
reactor.listenTCP(8080, site)
reactor.run()

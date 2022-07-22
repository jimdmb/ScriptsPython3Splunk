#mostly copied python script to do a splunk query

import urllib
import httplib2
import time
import re
from time import localtime,strftime
from xml.dom import minidom
import json

#put together from various sources, mostly other's code
#added to repository to supplement other scripts

baseurl = '[redacted]'
username = '[redacted]'
password = '[redacted]'
searchquery = 'search query'
myhttp = httplib2.Http(disable_ssl_certificate_validation=True)

#Step 1: Get a session key
servercontent = myhttp.request(baseurl + '/services/auth/login', 'POST',
headers={}, body=urllib.parse.urlencode({'username':username, 'password':password}))[1]
sessionkey = minidom.parseString(servercontent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
#print ("====>sessionkey:  %s  <====" % sessionkey)

#Step 2: Create a search job. remove wifi, vpn, perimeter
searchjob = myhttp.request(baseurl + '/services/search/jobs','POST',
headers={'Authorization': 'Splunk %s' % sessionkey},body=urllib.parse.urlencode({'search': searchquery}))[1]
sid = minidom.parseString(searchjob).getElementsByTagName('sid')[0].childNodes[0].nodeValue
#print ("====>sid:  %s  <====" % sid)

#Step 3: Get the search status
myhttp.add_credentials(username, password)
servicessearchstatusstr = '/services/search/jobs/%s/' % sid
isnotdone = True
while isnotdone:
   searchstatus = myhttp.request(baseurl + servicessearchstatusstr, 'GET')[1]
   searchstatus = str(searchstatus)
   if searchstatus.find('isDone">1') !=-1:
       isnotdone = False
#print ("====>search status:  %s  <====" % isdonestatus)

#Step 4: Get the search results
services_search_results_str = '/services/search/jobs/%s/results?output_mode=json&count=0' % sid
#services_search_results_str = '/services/search/jobs/%s/results' % sid
searchresults = myhttp.request(baseurl + services_search_results_str, 'GET')[1]
#print ("====>search result:  [%s]  <====" % searchresults)

############junk
y = json.loads(searchresults)
print(y)
for results in y['results']:
        for key,value in results.items():
                print (value)

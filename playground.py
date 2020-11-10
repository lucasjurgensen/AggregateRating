import urllib3
import xml.etree.ElementTree as ET

# Grab developer key
f = open("goodreads_key", "r")
dev_key = f.read()
f.close()

# Create URL
search_param = "Ender%27s+Game"
url = "https://www.goodreads.com/search.xml?key={}&q={}".format(dev_key, search_param)


# Get response
http = urllib3.PoolManager()
r = http.request('GET', url)
string_xml = r.data
root = ET.fromstring(string_xml)

# Process Response
for elem in root.iter("work"):
    for elem1 in elem.iter("title"):
        print(elem1.text)
import urllib3
import xml.etree.cElementTree as ET


# Grab developer key
f = open("goodreads_key", "r")
dev_key = f.read()
f.close()


###############
# Get reviews example
book_id = 375802 # Ender's Game
url = "https://www.goodreads.com/book/show.xml?key={}&id={}".format(dev_key, book_id)

# Get response
http = urllib3.PoolManager()
r = http.request('GET', url)
string_xml = r.data

print(string_xml)
root = ET.fromstring(string_xml)

# Process Response
print(root)
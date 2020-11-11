import urllib3
try:
    # cElementTree is a faster, c-based version
    import xml.etree.cElementTree as ET
except ImportError:
    # Resort to the standard, slower one if import fails
    import xml.etree.ElementTree as ET

# Grab developer key
f = open("goodreads_key", "r")
dev_key = f.read()
f.close()

############
# Search for book example
# Create URL
search_param = "Ender%27s+Game"
search_param = "The+Great+Gatsby"
url = "https://www.goodreads.com/search.xml?key={}&q={}".format(dev_key, search_param)


# Get response
http = urllib3.PoolManager()
r = http.request('GET', url)
string_xml = r.data
root = ET.fromstring(string_xml)

# Process Response
print("reached")
for book in root.iter(tag="best_book"):
    for id in book.iterfind("id"):
        print(id.text)
# for elem in root.iter("work"):
#     for elem1 in elem.iter("title"):
#         print(elem1.text)


###############
# Get reviews example
book_id = 18079759
url = "https://www.goodreads.com/book/show.xml?key={}&id={}".format(dev_key, book_id)

# Get response
http = urllib3.PoolManager()
r = http.request('GET', url)
string_xml = r.data
print(string_xml)
root = ET.fromstring(string_xml)

# Process Response
print(root)
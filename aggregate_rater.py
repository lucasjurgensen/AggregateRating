import urllib3
import xml.etree.cElementTree as ET

# Pull in dev key
f = open("goodreads_key", "r")
dev_key = f.read()
f.close()


##################
# Definitions
class book:
    title = ""
    id = ""
    def __init__(self, _title, _id):
        self.title = _title
        self.id = _id

class review:
    stars = -1
    text = ""

class user:
    name = ""
    id = ""
    reviews = []


##################
# Select Book
search_param = "Ender%27s+Game"
url = "https://www.goodreads.com/search.xml?key={}&q={}".format(dev_key, search_param)
http = urllib3.PoolManager()
r = http.request('Get', url)
string_xml = r.data
root = ET.fromstring(string_xml)

# Find the best book based on search
best_book_found = root.find("search").find("results").find("work").find("best_book")
book = book(_title=best_book_found.find("title").text, _id=best_book_found.find("id").text)
    # break

print(book.title)
print(book.id)


##################
# Get User Reviews
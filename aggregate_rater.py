import re
import xml.etree.cElementTree as ET
import api_manager

# Pull in dev key
f = open("goodreads_key", "r")
dev_key = f.read()
f.close()


##################
# Definitions

class Book:
    title = ""
    id = ""

    def __init__(self, _title, _id):
        self.title = _title
        self.id = _id

    def __repr__(self):
        return "{} - {}".format(self.title, self.id)

class Review:
    book = ""
    rating = -1
    text = ""

    def __init__(self, _title, _book_id, _rating):
        self.book = Book(_title, _book_id)
        self.rating = _rating

class User:
    name = ""
    id = ""
    reviews = []


##################
# Functions

def get_book_by_title(search_param="Ender's Game'"):
    escaped_search_param = re.sub('[^0-9a-zA-Z]+', '_', search_param)
    manager = api_manager.API_Manager()
    url = "https://www.goodreads.com/search.xml?key={}&q={}".format(dev_key, search_param)
    string_xml = manager.goodreads_get(url)
    root = ET.fromstring(string_xml)

    best_book_found = root.find("search").find("results").find("work").find("best_book")
    book = Book(_title=best_book_found.find("title").text, _id=best_book_found.find("id").text)

    print(book)
    return book

def get_user_bookshelf_reviews(user_id=120182276):
    manager = api_manager.API_Manager()
    url = "https://www.goodreads.com/review/list?v=2&id={}&shelf={}&per_page={}&key={}".format(user_id,"read","200",dev_key)
    string_xml = manager.goodreads_get(url)
    root = ET.fromstring(string_xml)

    reviews = []
    for review_full in root.find("reviews").findall("review"):
        review = Review(_title=review_full.find("book").find("title").text,
                        _book_id=review_full.find("book").find("id").text,
                        _rating=review_full.find("rating"))
        rating = review_full.find("rating")
        reviews.append(review)

    print(reviews)
    return reviews



##################

def main():
    get_book_by_title()
    get_user_bookshelf_reviews()

if __name__ == "__main__":
    main()
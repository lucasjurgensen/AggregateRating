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
    title = "" # type string
    id = "" # type string

    def __init__(self, _title, _id):
        self.title = _title
        self.id = _id

    def __eq__(self, other):
        # if self.title == "Sharp Objects":
        #     print(self.id, self.title, "vs", other.id, other.title, self.title == other.title)a
        return ((self.title == other.title) or (self.id == other.id))

    def __repr__(self):
        return "{} - {}".format(self.title, self.id)

class Review:
    book = "" # type Book
    rating = -1 # type int
    text = "" # type string

    def __init__(self, _book_title, _book_id, _rating):
        self.book = Book(_book_title, _book_id)
        self.rating = _rating

    # Equivalence of reviews refers only that they are reviewing the same book
    def __eq__(self, other):
        return (self.book == other.book)

class User:
    name = "" # type string
    id = "" # type string
    reviews = [] # type list of Review

    def __init__(self, _name, _id, _reviews):
        self.name = _name
        self.id = _id
        self.reviews = _reviews


##################
# Functions

def get_book_by_title(search_param="Ender's Game'"):
    escaped_search_param = re.sub('[^0-9a-zA-Z]+', '_', search_param)
    manager = api_manager.API_Manager()
    url = "https://www.goodreads.com/search.xml?key={}&q={}".format(dev_key, escaped_search_param)
    string_xml = manager.goodreads_get(url)
    root = ET.fromstring(string_xml)

    best_book_found = root.find("search").find("results").find("work").find("best_book")
    book = Book(_title=best_book_found.find("title").text, _id=best_book_found.find("id").text)

    return book

def get_user_bookshelf_reviews(user_id=120182276):
    manager = api_manager.API_Manager()
    url = "https://www.goodreads.com/review/list?v=2&id={}&shelf={}&per_page={}&key={}".format(user_id,"read","200",dev_key)
    string_xml = manager.goodreads_get(url)
    root = ET.fromstring(string_xml)

    reviews = []
    for review_full in root.find("reviews").findall("review"):
        # print(review_full.find("book").find("id").text)
        review = Review(_book_title=review_full.find("book").find("title").text,
                        _book_id=review_full.find("book").find("id").text,
                        _rating=review_full.find("rating"))
        # rating = review_full.find("rating")
        reviews.append(review)


    return reviews

def get_book_overlap_between_users(user_id_1=120182276, user_id_2=1113001):
    # Lucas id = 120182276
    # Random id = 1113001

    user_1_reviews = get_user_bookshelf_reviews(user_id_1)
    user_1 = User("", user_id_1, user_1_reviews)

    # print("X")

    user_2_reviews = get_user_bookshelf_reviews(user_id_2)
    user_2 = User("", user_id_2, user_2_reviews)

    user_1_unique = []
    user_2_unique = []
    shared = []

    for review in user_1.reviews:
        if review in user_2_reviews:
            shared.append(review)
        else:
            user_1_unique.append(review)

    for review in user_2.reviews:
        if review not in shared:
            user_2_unique.append(review)

    return (user_1_unique, user_2_unique, shared)



##################

def main():
    # get_book_by_title()
    # get_user_bookshelf_reviews()
    (a,b,c) = get_book_overlap_between_users()
    print(len(a))
    print(len(b))
    print(len(c))
    for x in c:
        print(x.book)

if __name__ == "__main__":
    main()
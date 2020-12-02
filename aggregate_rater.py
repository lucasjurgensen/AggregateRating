#!/usr/local/bin/python3

import argparse
import re
import time
import xml.etree.cElementTree as ET

import api_manager
import reviewers

# TODO - temporarily hardcode the key
# Pull in dev key
# f = open("goodreads_key", "r")
# dev_key = f.read()
# f.close()

# Hardcoding key for now
dev_key = "qcXIjujzhYVHOFU4SszgQ"

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

    def __repr__(self):
        return "{} - {}".format(self.book, self.rating)

class User:
    name = "" # type string
    id = "" # type string
    reviews = [] # type list of Review
    weight = 1

    def __init__(self, _name, _id, _reviews):
        self.name = _name
        self.id = _id
        self.reviews = _reviews
        self.weight = 1


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
    if root.text != "forbidden":
        for review_full in root.find("reviews").findall("review"):
            # print(review_full.find("book").find("id").text)
            review = Review(_book_title=review_full.find("book").find("title").text,
                            _book_id=review_full.find("book").find("id").text,
                            _rating=review_full.find("rating").text)
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
    shared_copy = []

    for review in user_1.reviews:
        if review in user_2_reviews:
            shared.append((review, user_2_reviews[user_2_reviews.index(review)]))
            shared_copy.append(review)
        else:
            user_1_unique.append(review)

    for review in user_2.reviews:
        if review not in shared_copy:
            user_2_unique.append(review)

    return (user_1_unique, user_2_unique, shared)

def weight(rating_1, rating_2):
    if rating_1 == 0 or rating_2 ==0:
        return 1

    delta = abs(rating_1-rating_2)
    if delta == 4:
        return 0.25
    if delta == 3:
        return 0.5
    if delta == 2:
        return 1
    if delta == 1:
        return 2
    if delta == 0:
        return 4

def weight_user(user_id, other_id):
    taste = 1
    for book_review_comparison in get_book_overlap_between_users(user_id, other_id)[2]:
        user_review = book_review_comparison[0]
        other_review = book_review_comparison[1]
        taste *= weight(int(user_review.rating), int(other_review.rating))
    return taste

##################

def get_book_parser():
    parser = argparse.ArgumentParser(description="Select book to score")
    parser.add_argument('book_name', type=str, help="The book name to score")
    return parser

##################

def main():
    # TODO remove hardcode user-id
    user_id = 120182276

    start = time.time()
    manager = api_manager.API_Manager()
    parser = get_book_parser()
    args = parser.parse_args()
    book_name = args.book_name

    book = get_book_by_title(book_name)

    reviewers_list = reviewers.main(book.id)
    reviewer_user_list = []
    for reviewer in reviewers_list:
        reviewer_id = reviewer.split("-")[0]
        reviewer_name = reviewer.split("-")[1]
        reviewer_user_list.append(User(reviewer_name, reviewer_id, get_user_bookshelf_reviews(reviewer_id)))

    for other in reviewer_user_list:
        other.weight = weight_user(user_id, other.id)

    for user in reviewer_user_list:
        print("User: {:<20} Weight: {:<3}".format(user.name, user.weight))

    end = time.time()
    print("Made {} api calls, took {} seconds".format(manager.number_of_calls, round(end-start, 2)))
    return

if __name__ == "__main__":
    main()
import time
import re
import json
import api_manager
from bs4 import BeautifulSoup


def path_from_url(url):
    split_url = url.split('?')
    return split_url[0]


def params_from_url(url):
    split_url = url.split('?')
    if len(split_url) > 1:
        query_str = split_url[1]
        return dict(x.split('=') for x in query_str.split('&'))
    return {}


def get_reviews_widget(book_id, user_id):
    client = api_manager.API_Manager()
    # get widget xml
    res_json = client.goodreads_get(
        'https://www.goodreads.com/book/show.json', query_params={'USER_ID': user_id, 'id': book_id})
    res_obj = json.loads(res_json)
    soup = BeautifulSoup(res_obj['reviews_widget'], 'html.parser')
    reviews_url = soup.iframe['src']
    return reviews_url


def reviewer_from_profile(html_str):
    review_tree = BeautifulSoup(html_str, 'html.parser')
    reviewer_url = review_tree.find('a', class_='userReview')['href']
    user_id = reviewer_url.split('?')[0].split('/')[-1]
    return user_id


def crawl_reviews_for_users(reviews_path, reviews_params):
    client = api_manager.API_Manager()
    # iterate over the pages until we see 'no reviews found'
    more_reviews = True
    page = 1
    reviewer_list = []

    #TODO - temporarily only run once
    # while more_reviews:

    reviews_params['page'] = page
    html_str = client.goodreads_get(
        reviews_path, query_params=reviews_params)
    html_tree = BeautifulSoup(html_str, 'html.parser')

    # some janky code to determine if there are no more reviews
    contents = html_tree.find('div', class_='gr_reviews_showing').contents
    for content in contents:
        if 'No reviews found' in content:
            more_reviews = False

    reviewer_elems = html_tree.find_all('span', class_='gr_review_by')
    x = 0
    for el in reviewer_elems:
        if x == 10:
            break
        else:
            # look at the 2nd item because the <a> el is preceded by the string 'Reviewed by '
            review_url = el.contents[1]['href']
            review_str = client.goodreads_get(review_url)
            reviewer_list.append(reviewer_from_profile(review_str))
            # print(reviewer_from_profile(review_str))
        x += 1
    page += 1

    return(reviewer_list)


def get_reviewers_from_book(book_id, user_id):
    reviews_url = get_reviews_widget(book_id, user_id)
    reviews_path = path_from_url(reviews_url)
    reviews_params = params_from_url(reviews_url)
    return crawl_reviews_for_users(reviews_path, reviews_params)


def main(book_id = 44767458, user_id = 125142460):
    # Default to Dune and Lucas' id
    return get_reviewers_from_book(book_id, user_id)


if __name__ == '__main__':
    main()

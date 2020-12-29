import json
import plotly

import pandas as pd
from book_app import app
from flask import render_template, request
from filtering.collaborative_filtering import make_recommendations_for_new_user, make_user_based_recommendation
from filtering.common import get_book_info, find_book_ids
from filtering.wrangle_data import return_figures

# read in data
books = pd.read_csv("data/books.csv")
ratings = pd.read_csv("data/ratings.csv")
user_book_rating = pd.read_pickle("data/user_book_list.pkl")

N_BEST_OF = 5 # number of best books to show


def books_liked_online(cookie_name_start="like_book_"):
    """Read the cookies for books the user already liked on the website.
    
    :param cookie_name_start: String with which the cookies stored start
    :type: str
    :return: Book ids the user has liked on the website based on cookies
    :rtype: list[int]
    """
    all_cookies = request.cookies.to_dict()
    books_in_cache = []
    for cookie_name in all_cookies.keys():
        if cookie_name.startswith(cookie_name_start):
            books_in_cache.append(cookie_name[len(cookie_name_start):]) # to only obtain the book_id

    return books_in_cache


def are_books_liked(book_ids):
    """Check if certain books are liked by the user of the website.
    
    :param book_ids: List of book ids to verify
    :type: list[str]
    :return: If a book is liked by the user or not
    :rtype: list[int/boolean]
    """
    # get books liked from the cookies
    books_in_cookies = books_liked_online()

    # in case book_ids is an int/not a list
    if not isinstance(book_ids, list):
        book_ids = [book_ids]

    books_liked = [] # store 1 or 0 for each book
    for book in book_ids:
        if book in books_in_cookies:
            books_liked.append(1)
        else:
            books_liked.append(0)

    return books_liked


# index webpage
@app.route('/')
@app.route('/index')
def index():
    # number of books and users
    n_books = books.shape[0]
    n_users = ratings.groupby(["user_id"]).count().shape[0]
    n_ratings = ratings.shape[0]

    # get plotly figures
    figures = return_figures(ratings)

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    # This will render the index.html Please see that file.
    return render_template('index.html', n_books=n_books, n_users=n_users, n_ratings=n_ratings,ids=ids,
                           figuresJSON=figuresJSON)
  

@app.route('/bestof')
def bestof():
    # get the top N_BEST_OF books
    book_ids = [str(book_id) for book_id in books["book_id"][:N_BEST_OF].to_list()]
    best_titles = books["title"][:N_BEST_OF].to_list()
    best_authors = books["authors"][:N_BEST_OF].to_list()
    best_img_urls = books["image_url"][:N_BEST_OF].to_list()

    # check if the books are already liked (visualization purpose)
    books_liked = are_books_liked(book_ids)

    # This will render the bestof.html Please see that file. 
    return render_template('bestof.html', best_books=zip(book_ids, books_liked, best_authors, best_titles, best_img_urls))


@app.route('/enteruserid')
def enteruserid():
    # This will render the enteruserid.html Please see that file. 
    return render_template('enteruserid.html')


@app.route('/userrecommendations')
def userrecommendations():
    # save user input in query
    query = int(request.args.get('query', '')) #TODO check validity

    # obtain the recommendations for the requested user
    recommendations = make_user_based_recommendation(query, user_book_rating)

    # obtain meta data of recommendations
    all_authors, all_titles, all_img_urls = get_book_info(recommendations, books)

    # This will render the userrecommendations.html Please see that file. 
    return render_template(
        'userrecommendations.html',
        query=query,
        recommendations=recommendations,
        recommendation_infos=zip(all_authors, all_titles, all_img_urls)
    )


@app.route('/find')
def find():
    # This will render the find.html Please see that file. 
    return render_template('find.html')


@app.route('/searchresults')
def searchresults():
    # save user input in query
    author = request.args.get('author', '')
    title = request.args.get('title', '')

    # find relevant books from the dataset
    related_book_ids = find_book_ids(books, author, title)
    all_authors, all_titles, all_img_urls = get_book_info(related_book_ids, books)

    # convert book ids to strings
    related_book_ids= [str(book_id) for book_id in related_book_ids]
    
    # check if the books are already liked (visualization purpose)
    books_liked = are_books_liked(related_book_ids)

    # This will render the searchresults.html Please see that file. 
    return render_template(
        'searchresults.html',
        author=author,
        title=title,
        books_found=zip(related_book_ids, books_liked, all_authors, all_titles, all_img_urls)
    )

@app.route('/myrecommendations')
def myrecommendations():
    # get liked books from cookies
    books_liked = books_liked_online()
    if len(books_liked) > 0:

        # get recommendations for the online user
        recommendations = make_recommendations_for_new_user(books_liked, user_book_rating)
        
        # obtain meta data of recommendations
        all_authors, all_titles, all_img_urls = get_book_info(recommendations, books)

        success = 1
    
    else:
        # if no books are liked, no recommendation can be made
        recommendations, all_authors, all_titles, all_img_urls = [], [], [], []
        success = 0

    # This will render the recommend.html Please see that file. 
    return render_template(
        'myrecommendations.html',
        rec_success=success,
        recommendations=recommendations,
        recommendation_infos=zip(all_authors, all_titles, all_img_urls)
    )
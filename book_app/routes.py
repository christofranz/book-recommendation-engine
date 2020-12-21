import os
import pandas as pd
from book_app import app
from flask import Flask, render_template, request
from filtering.collaborative_filtering import get_read_books, create_user_book_dict, make_user_based_recommendation, find_closest_neighbors
from filtering.common import get_book_info, find_book_ids

# dir_path = os.path.dirname(os.path.realpath(__file__))
# TODO: safe filepath handling
books = pd.read_csv("data/books.csv")
user_book_matrix = pd.read_pickle("data/user_book_matrix.pkl")
dist_df = pd.read_pickle("data/user_distance.pkl")
books_read = create_user_book_dict(user_book_matrix)

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    first_title = books.iloc[0].title
    return render_template('index.html', titles=[first_title])
  

@app.route('/bestof')
def bestof():
    best_titles = books["title"][:5].to_list()
    best_authors = books["authors"][:5].to_list()
    best_img_urls = books["image_url"][:5].to_list()
    # This will render the bestof.html Please see that file. 
    return render_template('bestof.html', best_books=zip(best_authors, best_titles, best_img_urls))


@app.route('/recommend')
def recommend():
    # save user input in query
    query = int(request.args.get('query', '')) #TODO check validity
    # obtain the recommendations for the requested user
    recommendations = make_user_based_recommendation(query, dist_df, user_book_matrix, get_read_books(user_book_matrix, query), books_read)

    # obtain meta data of recommendations
    all_authors, all_titles, all_img_urls = get_book_info(recommendations, books)

    # This will render the recommend.html Please see that file. 
    return render_template(
        'recommend.html',
        query=query,
        recommendations=recommendations,
        recommendation_infos=zip(all_authors, all_titles, all_img_urls)
    )


@app.route('/find')
def find():
    # save user input in query
    author = request.args.get('author', '')
    title = request.args.get('title', '')

    related_book_ids = find_book_ids(books, author, title)
    all_authors, all_titles, _ = get_book_info(related_book_ids, books)

    # This will render the find.html Please see that file. 
    return render_template(
        'find.html',
        author=author,
        title=title,
        books_found=zip(all_authors, all_titles)
    )
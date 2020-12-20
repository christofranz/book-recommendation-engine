import pandas
import numpy as np


def get_read_books(user_book_matrix, user_id):
    """TODO"""
    read_books = list(user_book_matrix.loc[user_id][~user_book_matrix.loc[user_id].isna()].keys())
    return read_books


def create_user_book_dict(user_book_matrix):
    """TODO"""
    all_users = user_book_matrix.index.to_numpy()
    books_read = {}
    for user in all_users:
        books_read[user] = get_read_books(user_book_matrix, user)
        
    return books_read


def find_closest_neighbors(user_id, dist_df):
    '''
    INPUT:
        user - (int) the user_id of the individual you want to find the closest users
    OUTPUT:
        closest_neighbors - an array of the id's of the users sorted from closest to farthest away
    '''
    # ties are treated arbitrary and just kept whichever was easiest to keep using the head method
    # ordering the neighbors e.g. according to books read might be better    
    closest_neighbors = list(dist_df[dist_df["user1"] == user_id].sort_values(["dist"], ascending=True)["user2"])
    closest_neighbors.remove(user_id)
    return closest_neighbors

def books_liked(user_id, user_book_matrix, books_read, min_rating=3):
    '''
    INPUT:
    user_id - the user_id of an individual as int
    min_rating - the minimum rating considered while still a movie is still a "like" and not a "dislike"
    OUTPUT:
    books_liked - an array of movies the user has read and liked
    '''
    book_ratings = user_book_matrix.loc[user_id][books_read[user_id]]
    books_liked = list(book_ratings[book_ratings >= min_rating].keys())
    return books_liked

def get_book_info(book_id, books):
    """TODO"""
    book_info = books.loc[books["book_id"]==book_id]
    authors = book_info.squeeze().authors
    title = book_info.squeeze().title
    img_url = book_info.squeeze().image_url
    return authors, title, img_url

def make_user_based_recommendation(user_id, dist_df, user_book_matrix, books_read_by_user, books_read, num_rec=10, min_rating=3):
    """TODO"""
    recommendations = []
    # books_read_by_user = books_read[user_id]
    for neighbor in find_closest_neighbors(user_id, dist_df):
        liked_by_neighbor = books_liked(neighbor, user_book_matrix, books_read, min_rating)
        books_not_read = list(np.setdiff1d(liked_by_neighbor, books_read_by_user, assume_unique=False))
        books_not_recommended = list(np.setdiff1d(books_not_read, recommendations, assume_unique=False))
        # book_lst = book_names(books_not_read)
        recommendations = recommendations + books_not_recommended
        if len(recommendations) >= num_rec:
            recommendations = recommendations[:num_rec]
            break

    return recommendations
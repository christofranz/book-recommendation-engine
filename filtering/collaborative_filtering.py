import pandas as pd
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


def compute_euclidean_dist_for_new_user(books_user_new, user2, user_book_rating):
    """TODO"""
    # books_user_new has to be a list of int
    user2_book_rating = user_book_rating[user_book_rating["user_id"]==user2]
    books_user2 = user2_book_rating["book_id"].to_list()
    both_read = sorted(list(set(books_user_new).intersection(books_user2)), reverse=False)

    ratings_new_user = np.full(len(both_read), 5) #TODO: take corresponding real ratings
    # select only the ratings of user2 for books both read
    ratings_user2 = []
    for book_id in both_read:
        ratings_user2.append(int(user2_book_rating[user2_book_rating["book_id"] == book_id]["rating"]))

    if len(both_read) >= 1:
        dist = np.linalg.norm(ratings_new_user-np.array(ratings_user2))
    else:
        dist = 10000*5 # highest possible difference
    return dist


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


def find_closest_neighbors_for_new_users(books_user_new, user_book_rating):
    """TODO"""   
    user2 = []
    dist = []
    for user_id2 in user_book_rating["user_id"].unique():
        d = compute_euclidean_dist_for_new_user(books_user_new, user_id2, user_book_rating)
        user2.append(user_id2)
        dist.append(d)
    
    dist_df = pd.DataFrame({"user2": user2, "dist": dist})
    print(dist_df[:20])
    closest_neighbors = list(dist_df.sort_values(["dist"], ascending=True)["user2"])
    
    return closest_neighbors


def get_books_liked_by_user(user_id, user_book_matrix, books_read, min_rating=3):
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

def get_books_liked_by_user_2(user_id, user_book_rating, min_rating):
    """TODO
    Based on the new data input structure of user_book_rating
    """
    user2_book_rating = user_book_rating[user_book_rating["user_id"]==user_id]
    books_liked = user2_book_rating[user2_book_rating["rating"] >= min_rating]["book_id"].to_list()
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
        liked_by_neighbor = get_books_liked_by_user(neighbor, user_book_matrix, books_read, min_rating)
        books_not_read = list(np.setdiff1d(liked_by_neighbor, books_read_by_user, assume_unique=False))
        books_not_recommended = list(np.setdiff1d(books_not_read, recommendations, assume_unique=False))

        recommendations = recommendations + books_not_recommended
        if len(recommendations) >= num_rec:
            recommendations = recommendations[:num_rec]
            break

    return recommendations


def make_recommendations_for_new_user(books_liked, user_book_rating, num_rec=10, min_rating=3):
    """TODO"""
    # convert liked books to int
    books_user_new = [int(book_id) for book_id in books_liked]

    recommendations = []
    # get recommendations from the closest neighbors
    for neighbor in find_closest_neighbors_for_new_users(books_user_new, user_book_rating):
        liked_by_neighbor = get_books_liked_by_user_2(neighbor, user_book_rating, min_rating)
        books_not_read = list(np.setdiff1d(liked_by_neighbor, books_user_new, assume_unique=False))
        books_not_recommended = list(np.setdiff1d(books_not_read, recommendations, assume_unique=False))

        recommendations = recommendations + books_not_recommended
        if len(recommendations) >= num_rec:
            recommendations = recommendations[:num_rec]
            break

    return recommendations
import pandas as pd
import numpy as np

from filtering.common import get_books_liked_by_user

def compute_euclidean_dist_for_user(user1_book_rating, books_user1, user2, user_book_rating):
    """Compute euclidean distance for two existing users from the dataset.
    
    :param user1_book_rating: Ratings of user1 for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :param books_user1: Books read by the user recommendations are requested for
    :type: List of ints
    :param user2: Id of the user for who the distance is calculated
    :type: int
    :param user_book_rating: Ratings of each user for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :return: Distance between user1 and user2
    :rtype: float
    """
    user2_book_rating = user_book_rating[user_book_rating["user_id"]==user2]
    books_user2 = user2_book_rating["book_id"].to_list()
    both_read = sorted(list(set(books_user1).intersection(books_user2)), reverse=False)

    # select only the ratings of user for books both read
    ratings_user1 = []
    ratings_user2 = []
    for book_id in both_read:
        ratings_user1.append(int(user1_book_rating[user1_book_rating["book_id"] == book_id]["rating"]))
        ratings_user2.append(int(user2_book_rating[user2_book_rating["book_id"] == book_id]["rating"]))

    if len(both_read) >= 1:
        dist = np.linalg.norm(np.array(ratings_user1)-np.array(ratings_user2))
    else:
        dist = 10000*5 # highest possible difference

    return dist


def compute_euclidean_dist_for_new_user(books_user_new, user2, user_book_rating):
    """Compute euclidean distance for a new and one existing user from the dataset.
    
    :param books_user_new: Book (ids) liked or rated by the new user
    :type: List of ints
    :param user2: Id of the user for who the distance is calculated
    :type: int
    :param user_book_rating: Ratings of each user for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :return: Distance between the new user and user2
    :rtype: float
    """
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


def find_closest_neighbors_for_user(user_id, user_book_rating, user1_book_rating, books_user1, break_point_close_neighbors=100, threshold=1.5):
    """Find the closest neighbor for a certain user from the dataset.
    
    :param user_id: User for which the closest neighbor will be find
    :type: int
    :param user_book_rating: Ratings of each user for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :param user1_book_rating: Ratings of user1 for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :param books_user1: Books read by the user recommendations are requested for
    :type: List of ints
    :param break_point_close_neighbors: Parameter to stop the search if enough similar users are found
    :type: int
    :param threshold: Parameter that defines a close neighbor
    :type: float
    :return: Closest neighbors for the requested user with closest first
    :rtype: List of ints
    """
    user2 = []
    dist = []
    n_close_neighbors = 0
    other_users = np.delete(user_book_rating["user_id"].unique(), [user_id])
    for user_id2 in other_users:
        d = compute_euclidean_dist_for_user(user1_book_rating, books_user1, user_id2, user_book_rating)
        user2.append(user_id2)
        dist.append(d)

        if d <= threshold:
            n_close_neighbors += 1
            if n_close_neighbors >= break_point_close_neighbors:
                break
    
    dist_df = pd.DataFrame({"user2": user2, "dist": dist})

    closest_neighbors = list(dist_df.sort_values(["dist"], ascending=True)["user2"])
    
    return closest_neighbors


def find_closest_neighbors_for_new_users(books_user_new, user_book_rating, break_point_close_neighbors=100, threshold=1.5):
    """Find the closest neighbor for a new user.
    
    :param books_user_new: Book (ids) liked or rated by the new user
    :type: List of ints
    :param user_book_rating: Ratings of each user for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :param break_point_close_neighbors: Parameter to stop the search if enough similar users are found
    :type: int
    :param threshold: Parameter that defines a close neighbor
    :type: float
    :return: Closest neighbors for the requested user with closest first
    :rtype: List of ints
    """   
    user2 = []
    dist = []
    n_close_neighbors = 0
    for user_id2 in user_book_rating["user_id"].unique():
        d = compute_euclidean_dist_for_new_user(books_user_new, user_id2, user_book_rating)
        user2.append(user_id2)
        dist.append(d)

        if d <= threshold:
            n_close_neighbors += 1
            if n_close_neighbors >= break_point_close_neighbors:
                break
    
    dist_df = pd.DataFrame({"user2": user2, "dist": dist})

    closest_neighbors = list(dist_df.sort_values(["dist"], ascending=True)["user2"])
    
    return closest_neighbors


def make_user_based_recommendation(user_id, user_book_rating, num_rec=10, min_rating=3):
    """Make book recommendations for an existing user from the dataset.

    :param user_id: User for which the closest neighbor will be find
    :type: int
    :param user_book_rating: Ratings of each user for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :param num_rec: Number of maximal recommendations for the user
    :tpye: int
    :param min_rating: Minimal rating that defines if a user liked a book
    :type: int
    :return: Book ids that are recommended for the user
    :rtype: List of ints    
    """
    recommendations = []
    user1_book_rating = user_book_rating[user_book_rating["user_id"]==user_id]
    books_user1 = user1_book_rating["book_id"].to_list()

    # books_read_by_user = books_read[user_id]
    for neighbor in find_closest_neighbors_for_user(user_id, user_book_rating, user1_book_rating, books_user1):
        liked_by_neighbor = get_books_liked_by_user(neighbor, user_book_rating, min_rating)
        books_not_read = list(np.setdiff1d(liked_by_neighbor, books_user1, assume_unique=False))
        books_not_recommended = list(np.setdiff1d(books_not_read, recommendations, assume_unique=False))

        recommendations = recommendations + books_not_recommended
        if len(recommendations) >= num_rec:
            recommendations = recommendations[:num_rec]
            break

    return recommendations


def make_recommendations_for_new_user(books_liked, user_book_rating, num_rec=10, min_rating=3):
    """Make book recommendations for an existing user from the dataset.

    :param books_liked: Book (ids) the new user liked
    :type: List of ints
    :param user_book_rating: Ratings of each user for each book read
    :type: pandas dataframe with cols ["user_id", "book_id", "rating"]
    :param num_rec: Number of maximal recommendations for the user
    :tpye: int
    :param min_rating: Minimal rating that defines if a user liked a book
    :type: int
    :return: Book ids that are recommended for the new user
    :rtype: List of ints    
    """
    # convert liked books to int
    books_user_new = [int(book_id) for book_id in books_liked]

    recommendations = []
    # get recommendations from the closest neighbors
    for neighbor in find_closest_neighbors_for_new_users(books_user_new, user_book_rating):
        liked_by_neighbor = get_books_liked_by_user(neighbor, user_book_rating, min_rating)
        books_not_read = list(np.setdiff1d(liked_by_neighbor, books_user_new, assume_unique=False))
        books_not_recommended = list(np.setdiff1d(books_not_read, recommendations, assume_unique=False))

        recommendations = recommendations + books_not_recommended
        if len(recommendations) >= num_rec:
            recommendations = recommendations[:num_rec]
            break

    return recommendations
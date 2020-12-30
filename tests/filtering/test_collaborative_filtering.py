import pytest
import pandas as pd
import numpy as np

from filtering.collaborative_filtering import compute_euclidean_dist_for_user, compute_euclidean_dist_for_new_user, find_closest_neighbors_for_user, find_closest_neighbors_for_new_users


@pytest.mark.parametrize("user2, expected_distance",
                        [(2, 3.162),
                        (3, 0)])
def test_compute_euclidean_dist_for_user(user2, expected_distance):
    """Test compute_euclidean_dist_for_user from filtering.collaborative_filtering."""
    book_id = [1, 2, 1, 2, 1, 6]
    user_ids = [1, 1, 2, 2, 3, 3]
    ratings = [2, 4, 1, 1, 2, 5]
    user_book_rating = pd.DataFrame(data=list(zip(book_id, user_ids, ratings)), columns=["book_id", "user_id", "rating"])
    user1_book_rating = user_book_rating[user_book_rating["user_id"] == 1]
    books_user1 = [1, 2]
    distance = compute_euclidean_dist_for_user(user1_book_rating, books_user1, user2, user_book_rating)

    assert np.isclose(distance, expected_distance, 0.001)


@pytest.mark.parametrize("books_user_new, user2, expected_distance",
                        [([1, 2], 1, 3.162),
                        ([7], 3, 10000*5),
                        ([8, 6], 3, 0),
                        ([2], 2, 4)])
def test_compute_euclidean_dist_for_new_user(books_user_new, user2, expected_distance):
    """Test compute_euclidean_dist_for_new_user from filtering.collaborative_filtering."""
    book_id = [1, 2, 1, 2, 1, 6]
    user_ids = [1, 1, 2, 2, 3, 3]
    ratings = [2, 4, 1, 1, 2, 5]
    user_book_rating = pd.DataFrame(data=list(zip(book_id, user_ids, ratings)), columns=["book_id", "user_id", "rating"])
    distance = compute_euclidean_dist_for_new_user(books_user_new, user2, user_book_rating)

    assert np.isclose(distance, expected_distance, 0.001)


@pytest.mark.parametrize("user_id, expected_neighbors",
                        [(1, [2, 3]),
                        (2, [3, 1]),
                        (3, [2, 1])])
def test_find_closest_neighbors_for_user(user_id, expected_neighbors):
    """Test find_closest_neighbors_for_user from filtering.collaborative_filtering."""
    book_id = [1, 2, 1, 2, 1, 6]
    user_ids = [1, 1, 2, 2, 3, 3]
    ratings = [4, 4, 2, 2, 1, 1]
    user_book_rating = pd.DataFrame(data=list(zip(book_id, user_ids, ratings)), columns=["book_id", "user_id", "rating"])
    user1_book_rating = user_book_rating[user_book_rating["user_id"] == user_id]
    books_user1 = user1_book_rating["book_id"]

    neighbors = find_closest_neighbors_for_user(user_id, user_book_rating, user1_book_rating, books_user1)

    assert np.array_equal(np.array(neighbors), np.array(expected_neighbors))


@pytest.mark.parametrize("books_user_new, expected_neighbors",
                        [([1, 2], [1, 3, 2]),
                        ([1], [1, 2, 3]),
                        ([1, 6], [1, 2, 3])])
def test_find_closest_neighbors_for_new_user(books_user_new, expected_neighbors):
    """Test find_closest_neighbors_for_new_users from filtering.collaborative_filtering."""
    book_id = [1, 2, 1, 2, 1, 6]
    user_ids = [1, 1, 2, 2, 3, 3]
    ratings = [4, 4, 2, 2, 1, 1]
    user_book_rating = pd.DataFrame(data=list(zip(book_id, user_ids, ratings)), columns=["book_id", "user_id", "rating"])

    neighbors = find_closest_neighbors_for_new_users(books_user_new, user_book_rating)

    assert np.array_equal(np.array(neighbors), np.array(expected_neighbors))
import pytest
import pandas as pd
import numpy as np

from filtering.common import get_book_info, get_books_liked_by_user, find_in_string, find_book_ids


@pytest.mark.parametrize("book_id, expected_book_authors, expected_book_titles, expected_book_img_urls",
                        [(1, ["abc"], ["my_book"], ["http1"]),
                        ([1], ["abc"], ["my_book"], ["http1"]),
                        ([2, 3, 4], ["abc", "def", "ghi"], ["your_book", "his_book", "her_book"], ["http2", "http3", "http4"])])
def test_get_book_info(book_id, expected_book_authors, expected_book_titles, expected_book_img_urls):
    """Test get_book_info from filtering.common."""
    book_ids = [1, 2, 3, 4]
    all_authors = ["abc", "abc", "def", "ghi"]
    all_titles = ["my_book", "your_book", "his_book", "her_book"]
    all_img_urls = ["http1", "http2", "http3", "http4"]
    books = pd.DataFrame(data=list(zip(book_ids, all_authors, all_titles, all_img_urls)), columns=["book_id", "authors", "title", "image_url"])
    authors, titles, img_urls = get_book_info(book_id, books)
    assert np.array_equal(authors, expected_book_authors)
    assert np.array_equal(titles, expected_book_titles)
    assert np.array_equal(img_urls, expected_book_img_urls)


@pytest.mark.parametrize("users, books, ratings, expected_books_liked",
                        [([1, 1, 1, 2], [1, 2, 3, 4], [2, 3, 4, 4], [2, 3]),
                        ([2, 2, 3, 4], [5, 6, 7, 8], [5, 5, 4, 1], []),
                        ([1, 2, 1, 2], [3, 4, 5, 6], [1, 2, 1, 1], []),
                        ([1, 1, 1, 1], [1, 2, 3, 4], [3, 3, 3, 3], [1, 2, 3, 4])])
def test_get_books_liked_by_user(users, books, ratings, expected_books_liked):
    """Test get_books_liked_by_user from filtering.common."""
    user_id = 1
    # create input for the function
    user_book_rating = pd.DataFrame(data=list(zip(users, books, ratings)), columns=["user_id", "book_id", "rating"])
    # obtain liked books and compare results
    books_liked = get_books_liked_by_user(user_id, user_book_rating, 3)
    assert np.array_equal(np.array(books_liked), np.array(expected_books_liked))


@pytest.mark.parametrize("sub, string, expected_result",
                        [("test", "test_string", 1),
                        ("TEST", "test_string", 1),
                        ("test", "TEST", 1),
                        ("test", "string", 0),
                        ("t3st", "test_string", 0)])
def test_find_in_string(sub, string, expected_result):
    """Test find_in_string from filtering.common."""
    result = find_in_string(sub, string)
    assert result == expected_result


@pytest.mark.parametrize("search_authors, search_title, expected_book_ids",
                        [("abc", "book", [1, 5]),
                        ("abc", "my", [1]),
                        (None, "my", [1]),
                        ("def", None, [2, 3]),
                        ("ghi", "no", [])])
def test_find_book_ids(search_authors, search_title, expected_book_ids):
    """Test find_book_ids from filtering.common."""
    book_ids = [1, 2, 3, 4, 5]
    authors = ["abc", "def", "def", "ghi", "abc"]
    titles = ["my_book", "your_book", "his_book", "her_book", "their_book"]
    books = pd.DataFrame(data=list(zip(book_ids, authors, titles)), columns=["book_id", "authors", "title"])
    found_books = find_book_ids(books, search_authors, search_title)

    assert np.array_equal(np.array(found_books), np.array(expected_book_ids))
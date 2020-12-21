def get_book_info(book_id, books):
    """TODO"""
    if not isinstance(book_id, list):
        book_id = [book_id]
    book_authors, book_titles, book_img_urls = [], [], []
    for i in book_id:
        book_info = books.loc[books["book_id"]==i].squeeze()
        book_authors.append(book_info.authors)
        book_titles.append(book_info.title)
        book_img_urls.append(book_info.image_url)
    
    return book_authors, book_titles, book_img_urls


def find_in_string(sub, string):
    """Check if a substring is contained in another string.    """
    sub_l = sub.lower()
    string_l = string.lower()
    if sub_l in string_l or string_l in sub_l:
        return 1
    else:
        return 0


def find_book_ids(books, author=None, title=None, dist_thresh=0.7):
    """TODO"""
    if not author and not title:
        print("Please add an author and/or a title.")
    else:
        book_candidates = []
        all_authors = books["authors"].to_list()
        all_titles = books["title"].to_list()
        if author is not None:
            # find all books with this author
            for idx, a in enumerate(all_authors):
                dist_a = find_in_string(author, a) #TODO: alternative distance function
                if dist_a >= dist_thresh:
                    book_candidates.append(books.iloc[idx]["book_id"])

            # iterate over books from author
            relevant_book_ids = book_candidates.copy()

            if title:
                titles_from_author = []
                for book_id in book_candidates:
                    t = books.loc[books["book_id"]==book_id].squeeze().title
                    dist_t = find_in_string(t, title)
                    if dist_t < dist_thresh:
                        relevant_book_ids.remove(book_id)

        else:
            # if author is not given, go only through titles
            relevant_book_ids = []
            for idx, t in enumerate(all_titles):
                dist_t = find_in_string(title, t)
                if dist_t >= dist_thresh:
                    relevant_book_ids.append(books.iloc[idx]["book_id"])

        return relevant_book_ids
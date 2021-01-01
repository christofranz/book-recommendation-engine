# Book-Recommendation-Engine

### Table of Contents

1. [Installation and Instructions](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing](#licensing)

## Installation and Instructions<a name="installation"></a>

### Installation

You will need the standard data science libraries found in the Anaconda distribution of Python. Especially, the following packages are required:

- NumPy
- Pandas
- Plotly
- Pytest
- Flask

If you want to run the jupyter notebooks, you will also need to install:

- jupyter notebook
- Matplotlib
- Seaborn

Alternatively, you can directly install them with `pip install -r requirements_full.txt`. The code should run with no issues using Python versions 3.8.* or higher.
  
The data used in the webapp is partially stored on git lfs. Hence you need to [download and install git lfs](https://docs.github.com/en/free-pro-team@latest/github/managing-large-files/installing-git-large-file-storage).

### Instructions

1. Run the following command in the project's root directory to launch the webapp.
    `python book_app.py`

2. Go to http://0.0.0.0:3001/ 

    - You see the main page of the webapp. Here you can understand the data, find books and get your own recommendations.

## Project Motivation<a name="motivation"></a>

This project shall be a prototype for a book recommendation engine that allows an interaction of the user with the database to get personalized recommendations. Finding the next interesting book can become a challenge and recommendation engines support the user to find the right book. The user based implemented approach recommends books based on the users from the dataset who are most similar and books they liked and the user has not read yet.

## File Descriptions <a name="files"></a>

The most important files in this repository:

* `book_app.py` - This python file hosts the webapp via flask.

* `data_inspection.ipynb` - Jupyter notebook for initial data inspection.

* `collaborative_filtering.ipynb` - Jupyter notebook for initial recommendation engine development.

* `filtering/common.py` - Contains common python functions that can be used independent of the concrete filtering method.

* `filtering/collaborative_filtering.py` - The core of the recommendation system is contained in this python file.

* `filtering/wrangle_data.py` - Creates the plotly visualizations of the webapp.

* `data/books.csv` - Csv-file with books and meta data.

* `data/ratings.csv` - Csv-file with all ratings from the users for the books.

* `data/user_book_list.pkl` - Pickle-file with all users, the books read and the corresponding ratings. Transformation of `ratings.csv`.

* `book_app/routes.py` - Defines the routes for the flask app and renders the html files.

* `book_app/templates/` - Contains the html files of the webapp.

* `book_app/static/img/` - Contains images used in the webapp.

* `book_app/static/styles/` - Contains css-files to format the style of the webpages.

* `tests/filtering/` - Contains unit tests.

## Results<a name="results"></a>

The webapp offers the possibility to understand the data (distribution of ratings per book and user, histogram of ratings), inspect the most popular books from the dataset and find books by author and/or title. Additionally, you can like books from the search and be used to get your own recommendations. The likes are stored over different sessions because they are stored in the cookies.

### Screenshots

![Header](documentation/images/header.png)
![Data Analysis](documentation/images/data.png)
![Search Books](documentation/images/search.png)
![Individual Recommendations](documentation/images/individual_recommendations.png)

## Licensing<a name="licensing"></a>
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
The data was prepared and uploaded by [zygmuntz](https://github.com/zygmuntz/goodbooks-10k/) to github.
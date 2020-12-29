import plotly.graph_objs as go

def return_figures(ratings):
    """Create plotly visualizations for webapp.

    :param ratings: Dataframe containing the ratings
    :type: Pandas dataframe with columns ["user_id", "book_id", "rating"]
    :return: List containing the plotly visualizations
    :rtype: List (dict)
    """
    # histogram for the distribution of ratings
    graph_one = [go.Histogram(x=ratings["rating"],
                marker_color='#568cbf',
                opacity=0.75)]
    layout_one = dict(title = 'Distribution of Ratings',
                xaxis = dict(title = 'Rating Value', tick0 = 1,
                    dtick = 1),
                yaxis = dict(title = 'Occurances'),
                bargap=0.05,
                )

    ratings_per_user = ratings.groupby(["user_id"]).count()["rating"].reset_index(name="rating_counts")

    # histogram for the distribution of ratings per user
    graph_two = [go.Histogram(x=ratings_per_user["rating_counts"],
                xbins=dict(
                    size=10
                ),
                marker_color='#EB89B5',
                opacity=0.75)]
    layout_two = dict(title = 'Ratings Per User',
                xaxis = dict(title = 'Number of Ratings'),
                yaxis = dict(title = 'Number of Users'),
                bargap=0.05,
                )
    
    # histogram for the distribution of ratings per book
    ratings_per_book = ratings.groupby(["book_id"]).count()["rating"].reset_index(name="rating_counts")
    graph_three = [go.Histogram(x=ratings_per_book["rating_counts"],
                xbins=dict(
                    start=0,
                    end=2000,
                    size=100
                ),
                marker_color='#5fe8a4',
                opacity=0.75)]
    layout_three = dict(title = 'Ratings Per Book',
                xaxis = dict(title = 'Number of Ratings'),
                yaxis = dict(title = 'Number of Books'),
                bargap=0.05,
                )

    # add data and layout to figures
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))    
   
    return figures
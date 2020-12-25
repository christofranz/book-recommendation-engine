import pandas as pd
import plotly.graph_objs as go

def return_figures(books, ratings):
    """Creates plotly visualizations

    Args:
        TODO

    Returns:
        list (dict): list containing the plotly visualizations

    """
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

    # second chart plots ararble land for 2015 as a bar chart    
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
    # # world map
    
    # graph_five = []
    # graph_five.append(go.Choropleth(
    #     locations = df_merged['countryterritoryCode'],
    #     z = df_merged['cases'],
    #     text = df_merged['countriesAndTerritories'],
    #     colorscale = 'Blues',
    #     autocolorscale=False,
    #     reversescale=False))

    # layout_five = dict(title = 'Confirmed COVID-19 cases 20/04/08',
    #             title_x=0.5,
    #             geo=dict(
    #                 showframe=False,
    #                 showcoastlines=False,
    #                 projection_type='equirectangular'
    #             ),
    #             marker_line_color='darkgray',
    #             marker_line_width=0.5,
    #             colorbar_tickprefix = '',
    #             colorbar_title = 'Confirmed Cases',
    #             annotations = [dict(
    #                 x=0.55,
    #                 y=0.1,
    #                 xref='paper',
    #                 yref='paper',
    #                 text='Source: <a href="https://data.europa.eu/euodp/de/data/dataset/covid-19-coronavirus-data">data.europe</a>',
    #                 showarrow = False)]
    #             )
    
    
    
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    # figures.append(dict(data=graph_five, layout=layout_five))                               
    
   
    return figures
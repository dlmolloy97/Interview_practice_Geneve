import dash
import folium
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import pandas as pd
import numpy as np
import folium
import branca
import branca.colormap as cm
def map_filter(df, max_price, total_nights):
    quantiles=df['price'].quantile(q=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8, 0.9])
    df=df[df['price']<=max_price]
    colormap = cm.linear.RdBu_11.scale(df['price'].min(),df['price'].max()).to_step(n=10,quantiles = quantiles)
    map = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=14,control_scale=True)
    lat = list(df.latitude)
    lon = list(df.longitude)
    pow = list(df.price)
    for loc, p in zip(zip(lat, lon), pow):
        folium.Circle(
        location=loc,
        radius=10,
        fill=True,
        color=colormap(p),
            popup = "Price per night: CHF {0}. Total price: CHF {1}".format(p, total_nights*p),
        fill_opacity=0.7).add_to(map)
    map.add_child(colormap)
    folium.TileLayer('cartodbpositron').add_to(map)
    map.save("Airbnb_map.html")
    return open('Airbnb_map.html','r').read()
listings = pd.read_csv('data/listings.csv')
# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    html.Div(
        className="row",
        children=[
            
            html.Div(
                className="six columns",
                style={'width': '60%', 'height':'150%','display': 'inline-block'},
                children=html.Div(
                    children=html.Iframe(id = 'map',srcDoc = map_filter(listings,400,20),width = '100%', height = '600'),
                )
            ),
            html.Div(
                className="six columns",
                style={'width': '40%', 'display': 'inline-block'},
                children=[
                    html.Div(children=[html.H1('Map of Geneva AirBNB'),html.Span("Maximum price per night"),
                    daq.NumericInput(id = 'daily_price',min=0, max=3000,value=200, size = 120),html.Span("Maximum total price for trip"),
                    daq.NumericInput(id = 'max_price',min=0, max=3000,value=1200, size = 120),
                    html.Span("Planned length of trip"),
                    daq.NumericInput(id = 'planned_stay',min=0, max=7,value=5, size = 120)]),
                html.Div(children = html.P("The user can use this tool to filter AirBNB listings in the city of Geneva by price per night (while setting a maximum total budget) while specifying the intended length of their stay. The map color-codes listings according to nightly price, with color steps defined by the quantiles of the (unfiltered) price distribution. "))])
        ]
    )
])
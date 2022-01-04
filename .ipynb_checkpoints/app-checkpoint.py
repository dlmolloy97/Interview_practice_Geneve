from multipart import app
import pandas as pd
import pandas as pd
import numpy as np
import folium
import branca
import branca.colormap as cm
import dash
import folium
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
listings = pd.read_csv('data/listings.csv')
@app.callback(Output('map', 'srcDoc'),[Input('daily_price', 'value'),Input('max_price', 'value'),Input('planned_stay', 'value')])
def map_opener(daily_price, max_price, planned_stay):
    df=listings[listings['price']<=daily_price]
    quantiles=df['price'].quantile(q=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8, 0.9])
    df=df[df['price']*planned_stay <= max_price]
    colormap = cm.linear.RdBu_11.scale(df['price'].min(),df['price'].max()).to_step(n=10,quantiles=quantiles)
    #colormap = cm.LinearColormap(colors=['blue','green','red'],vmin=0,vmax=3000)
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
            popup = "Price per night: CHF {0}.".format(p),
        fill_opacity=0.7
    ).add_to(map)
    map.add_child(colormap)
    folium.TileLayer('cartodbpositron').add_to(map)
    map.save("Airbnb_map.html")
    return open('Airbnb_map.html','r').read()

if __name__ == '__main__':
    app.run_server(debug=True,
                  port=8128,
                  use_reloader=False)
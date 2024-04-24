""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template, request

import folium
from folium import plugins

app = Flask(__name__)

# @app.route("/")
# def base():
#     # this is base map
#     map = folium.Map(
#         location=[45.5019, 73.5674],
#         zoom_start=6,
#         control_scale=True  # Adds a scale at the corner of the map
#     )
#     L.tileLayer.provider('Stadia.StamenWatercolor').addTo(map)

#     return map._repr_html_()

@app.route("/jawg")
def jawg_map():
    jawg_access_token = 'WMAqNzaloerLaxYEYXksWqAYggjkIOhiavg4Wpoz9nU8OxEhhlwb0fWViOQ9tOvp'
    jawg_tile_url = 'https://tile.jawg.io/jawg-streets/{z}/{x}/{y}{r}.png?access-token=WMAqNzaloerLaxYEYXksWqAYggjkIOhiavg4Wpoz9nU8OxEhhlwb0fWViOQ9tOvp'

    map = folium.Map(
        location=[45.53462, -73.55327],
        tiles=jawg_tile_url,
        attr='Jawg attribution',
        API_key=jawg_access_token,
        zoom_start=12,
        control_scale=True  # Adds a scale at the corner of the map
    )

    # Add the full screen button.                                               
    plugins.Fullscreen(                                                         
            position                = "topright",                                   
            title                   = "Open full-screen map",                       
            title_cancel            = "Close full-screen map",                      
            force_separate_button   = True,                                         
    ).add_to(map) 

    # Add the tracking location feature directly in Folium
    folium.plugins.LocateControl(
        position="topleft"
    ).add_to(map)

    # map.get_root().html.add_child(folium.Element('<style>#map{width: 100%; height: 100%; position: absolute; top: 0; bottom: 0; left: 0; right: 0;}</style>'))

    # # Save or render the map
    # map.save('map.html')  # If you are saving it directly

    # Pass map to the template
    map_html = map._repr_html_()
    return render_template('map.html', map_html=map_html)

@app.route("/", methods=["GET"])
def base():
    jawg_access_token = 'WMAqNzaloerLaxYEYXksWqAYggjkIOhiavg4Wpoz9nU8OxEhhlwb0fWViOQ9tOvp'
    jawg_tile_url = 'https://tile.jawg.io/jawg-streets/{z}/{x}/{y}{r}.png?access-token=WMAqNzaloerLaxYEYXksWqAYggjkIOhiavg4Wpoz9nU8OxEhhlwb0fWViOQ9tOvp'

    map = folium.Map(
        location=[45.53462, -73.55327],
        tiles=jawg_tile_url,
        attr='Jawg attribution',
        API_key=jawg_access_token,
        zoom_start=6,
        control_scale=True  # Adds a scale at the corner of the map
    )

    # Add the full screen button.                                               
    plugins.Fullscreen(                                                         
            position                = "topright",                                   
            title                   = "Open full-screen map",                       
            title_cancel            = "Close full-screen map",                      
            force_separate_button   = True,                                         
    ).add_to(map) 

    folium.plugins.Geocoder().add_to(map)

    # Add the tracking location feature directly in Folium
    folium.plugins.LocateControl(
        position="topleft"
    ).add_to(map)
    map_html = map._repr_html_()
    return render_template('map.html', map_html=map_html)

@app.route("/update_map", methods=["POST"])
def update_map():
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])

    map = folium.Map(
        location=[latitude, longitude],
        zoom_start=12,
        control_scale=True
    )
    jawg_access_token = 'WMAqNzaloerLaxYEYXksWqAYggjkIOhiavg4Wpoz9nU8OxEhhlwb0fWViOQ9tOvp'
    jawg_tile_url = 'https://tile.jawg.io/jawg-streets/{z}/{x}/{y}{r}.png?access-token=WMAqNzaloerLaxYEYXksWqAYggjkIOhiavg4Wpoz9nU8OxEhhlwb0fWViOQ9tOvp'

    map = folium.Map(
        location=[latitude, longitude],
        tiles=jawg_tile_url,
        attr='Jawg attribution',
        API_key=jawg_access_token,
        zoom_start=12,
        control_scale=True  # Adds a scale at the corner of the map
    )

    # Add the full screen button.                                               
    plugins.Fullscreen(                                                         
            position                = "topleft",                                   
            title                   = "Open full-screen map",                       
            title_cancel            = "Close full-screen map",                      
            force_separate_button   = True,                                         
    ).add_to(map) 

    folium.plugins.Geocoder().add_to(map)

    # Add the tracking location feature directly in Folium
    folium.plugins.LocateControl(
        position="topleft"
    ).add_to(map)
    map_html = map._repr_html_()
    return render_template('map.html', map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)
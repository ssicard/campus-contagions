import googlemaps
from datetime import datetime
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from key import api_key

################### Set Globals  #########################

app = Flask(__name__, template_folder=".")
app.config['GOOGLEMAPS_KEY'] = api_key
GoogleMaps(app)
gmaps = googlemaps.Client(key=api_key)

################### Set Directions  #########################

directions_result = gmaps.directions("Houston, TX", "Baton Rouge, LA")

################### Set Variables  #########################

locations1 = [(37.4419, -96.3413), (37.4419, -96.3410)]
mylocation = {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 30.6123, 
             'lng': -96.3413,
             'infobox': "<b>Where You Are</b>"
          }
defaultdoc = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': 30.6156, 
            'lng': -96.3427,
            'infobox': "<b>My Doctor</b>"
          }
batonrouge = {
			'lat':30.4515,
			'lng':-91.1971
		  }

################### Set Doctor Map  #########################

@app.route("/")
def mapview():
    doctormap = Map(
        identifier="doctormap",
        lat= 30.6123, 
        lng= -96.3413,
        markers=[mylocation, defaultdoc],
        #center_on_user_location = True,
        fit_markers_to_bounds = True,
        maptype_control = False,
        streetview_control = False,
        fullscreen_control = False
    )
    return render_template('index.html', doctormap=doctormap)

if __name__ == '__main__':
    app.run(debug=True)


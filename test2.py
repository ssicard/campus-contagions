from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

#from datetime import datetime

app = Flask(__name__, template_folder=".")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyD8YhyiKR0S4FAC91f6L5bWDLROOh723pE"
GoogleMaps(app)

campusmarkers = [(37.4419, -96.3413), (37.4419, -96.3410)]

@app.route("/")
def mapview():
    # creating a map in the view
    campusmap = Map(
        identifier="view-side",
     	lat= 30.6123, 
        lng= -96.3413,
        markers=[(37.4419, -96.3413)]
    )
    doctormap = Map(
        identifier="doctormap",
        lat= 30.6123, 
        lng= -96.3413,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 30.6123, 
             'lng': -96.3413,
             'infobox': "<b>Where I am</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            'lat': 30.6123, 
             'lng': -96.3333,
             'infobox': "<b>My Doctor</b>"
          }
        ]
    )
    return render_template('index.html', campusmap=campusmap, doctormap=doctormap)

if __name__ == '__main__':
    app.run(debug=True)


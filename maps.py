from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flaskext.mysql import MySQL
import googlemaps
from key import api_key, db_pass

app = Flask(__name__, template_folder=".")
app.config['GOOGLEMAPS_KEY'] = api_key
GoogleMaps(app)
gmaps = googlemaps.Client(key=api_key)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = db_pass
app.config['MYSQL_DATABASE_DB'] = 'maindb'
app.config['MYSQL_DATABASE_HOST'] = '35.193.222.83'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def mapview():
    all_symptom_locations = []
    cursor.execute("SELECT latitude, longitude, symptoms, disease FROM symptom")
    result = cursor.fetchall()
    for item in result:
        symptom = {'lat' : item[0], 'lng' : item[1], 'infobox' : 'symptoms: ' + item[2] if item[3] is None else 'disease: ' + item[3] }
        all_symptom_locations.append(symptom)

    all_hospitals = []
    result = gmaps.places_nearby(location=(30.6123,-96.3413), radius=16094, type='hospital')
    for hospital in result.get("results"):
        lat = hospital.get("geometry").get("location").get("lat")
        lng = hospital.get("geometry").get("location").get("lng")
        place = {'lat' : lat, 'lng' : lng, 'infobox' : hospital.get("name") }
        all_hospitals.append(place)

    # creating a map in the view
    campusmap = Map(
        identifier="campusmap",
     	lat= 30.6123, 
        lng= -96.3413,
        markers = all_symptom_locations,
        fit_markers_to_bounds = True,
        maptype_control = False,
        streetview_control = False,
        style = "height:400px;width:400px;margin:0;"
    )
    doctormap = Map(
        identifier = "doctormap",
        lat = 30.6123, 
        lng = -96.3413,
        markers = all_hospitals,
        fit_markers_to_bounds = True,
        maptype_control = False,
        streetview_control = False,
        style = "height:400px;width:400px;margin:0;"
    )
    return render_template('index.html', campusmap=campusmap, doctormap=doctormap)

if __name__ == '__main__':
    app.run(debug=True)


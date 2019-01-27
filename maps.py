from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flaskext.mysql import MySQL
#  import pymysql

app = Flask(__name__, template_folder=".")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyD8YhyiKR0S4FAC91f6L5bWDLROOh723pE"
GoogleMaps(app)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'INSERTROOTPASSWORDHERE'
app.config['MYSQL_DATABASE_DB'] = 'maindb'
app.config['MYSQL_DATABASE_HOST'] = '35.193.222.83'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def mapview():
    all_locations = []
    cursor.execute("SELECT latitude, longitude FROM symptom")
    result = cursor.fetchall()
    for item in result:
        all_locations.append(item)

    # creating a map in the view
    campusmap = Map(
        identifier="view-side",
     	lat= 30.6123, 
        lng= -96.3413,
        markers = all_locations,
        fit_markers_to_bounds = True
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


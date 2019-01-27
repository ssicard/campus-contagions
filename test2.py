import googlemaps
from datetime import datetime
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import json
from key import api_key, db_pass
from flaskext.mysql import MySQL

################### Set Globals  #########################

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = api_key
GoogleMaps(app)
gmaps = googlemaps.Client(key=api_key)

################### MySQL Configurations  #########################
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = db_pass
app.config['MYSQL_DATABASE_DB'] = 'maindb'
app.config['MYSQL_DATABASE_HOST'] = '35.193.222.83'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

################### Set Static Variables  #########################

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


all_hospitals = []
result = gmaps.places_nearby(location=(30.6123,-96.3413), radius=16094, type='hospital')
for hospital in result.get("results"):
    lat = hospital.get("geometry").get("location").get("lat")
    lng = hospital.get("geometry").get("location").get("lng")
    place = {'lat' : lat, 'lng' : lng, 'infobox' : hospital.get("name") }
    all_hospitals.append(place)

################### Set Routes  #########################

@app.route("/")
@app.route('/index')
@app.route('/signin')
def signin():
  return render_template('signin.html')

@app.route('/create')
def create():
  return render_template('create.html')

@app.route('/mapview')
def mapview():
    all_symptom_locations = []
    cursor.execute("SELECT latitude, longitude, symptoms, disease FROM symptom")
    result = cursor.fetchall()
    for item in result:
        symptom = {'icon':'http://maps.google.com/mapfiles/ms/icons/orange-dot.png','lat' : item[0], 'lng' : item[1], 'infobox' : 'symptoms: ' + item[2] if item[3] is None else 'disease: ' + item[3] }
        all_symptom_locations.append(symptom)

    all_hospitals = []
    result = gmaps.places_nearby(location=(30.6123,-96.3413), radius=16094, type='hospital')
    for hospital in result.get("results"):
        lat = hospital.get("geometry").get("location").get("lat")
        lng = hospital.get("geometry").get("location").get("lng")
        place = {'lat' : lat, 'lng' : lng, 'infobox' : hospital.get("name"),'icon':'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'}
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
    return render_template('maps.html', campusmap=campusmap, doctormap=doctormap)



@app.route('/diagnostics',methods=['GET','POST'])
def diagnostics():
    string = request.form['symptoms']
    gender = request.form['gender']
    yob = request.form['yob']
    return str(string)

@app.route('/create_user',methods=['GET','POST'])
def create_user():
    user = str(request.form['username'])
    secret = str(request.form['password'])
    gender = str(request.form['gender'])
    yearofbirth = str(request.form['year'])
    cursor.execute("INSERT INTO user(username, password_hash, sex, birthyear) VALUES ({{user}}, {{secret}}, {{gender}}, {{yearofbirth}})")
    return yearofbirth



if __name__ == '__main__':
    app.run(debug=True)


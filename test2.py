import googlemaps
from datetime import datetime
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import json
from key import api_key, db_pass
from flaskext.mysql import MySQL
from diagnose import getDiagnosisResults
import geocoder
import random
import decimal

symptomList = []

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

current_loc = geocoder.ip('me')
lat_lng = current_loc.latlng
my_lat = lat_lng[0]
my_lng = lat_lng[1]


def anonymize(val):
    num = float(decimal.Decimal(random.randrange(30, 110))/10000)
    if bool(random.getrandbits(1)):
        val += num
    else:
        val -= num
    return val


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
        symptom = {'icon':'http://maps.google.com/mapfiles/ms/icons/orange-dot.png','lat' : anonymize(item[0]), 'lng' : anonymize(item[1]), 'infobox' : 'symptoms: ' + item[2] }
        all_symptom_locations.append(symptom)

    all_hospitals = []
    result = gmaps.places_nearby(location=(my_lat,my_lng), radius=16094, type='hospital')
    for hospital in result.get("results"):
        lat = hospital.get("geometry").get("location").get("lat")
        lng = hospital.get("geometry").get("location").get("lng")
        place = {'lat' : lat, 'lng' : lng, 'infobox' : hospital.get("name"),'icon':'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'}
        all_hospitals.append(place)

    # creating a map in the view
    campusmap = Map(
        identifier="campusmap",
        lat= my_lat, 
        lng= my_lng,
        markers = all_symptom_locations,
        fit_markers_to_bounds = True,
        maptype_control = False,
        streetview_control = False,
        style = "height:400px;width:400px;margin:0;"
    )
    doctormap = Map(
        identifier = "doctormap",
        lat = my_lat, 
        lng = my_lng,
        markers = all_hospitals,
        fit_markers_to_bounds = True,
        maptype_control = False,
        streetview_control = False,
        style = "height:400px;width:400px;margin:0;"
    )
    return render_template('maps.html', campusmap=campusmap, doctormap=doctormap)



@app.route('/diagnostics',methods=['GET','POST'])
def diagnostics():
    text = request.form['input']
    diagnosisResults,symptomList = getDiagnosisResults(text, 'male', '1984')
    for symptom in symptomList:
        cursor.execute('INSERT INTO `symptom` (`latitude`,`longitude`,`time_checked`,`symptoms`,`disease`) VALUES (' + str(my_lat) + ',' + str(my_lng) + ',\"' + str(datetime.now()) + '\",\"' + symptom + '\", \"\");')
        conn.commit()
    return (str(len(symptomList)) + str(len(diagnosisResults)))
'''
    class symptomForm(Form):
    entry = StringField('')
form = symptomForm()
    return render_template('maps.html',form=form)
'''



if __name__ == '__main__':
    app.run(debug=True)


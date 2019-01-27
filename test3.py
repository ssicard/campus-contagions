import json, urllib
from urllib import urlencode
import googlemaps
from key import api_key
start = "Bridgewater, Sa, Australia"
finish = "Stirling, SA, Australia"


gmaps = googlemaps.Client(key=api_key)
#################################### DIRECTIONS ###########################
# url = 'https://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
#             ('origin', start),
#             ('destination', finish),
#             ('key', api_key)
#  ))
# print url
# ur = urllib.urlopen(url)
# result = json.load(ur)

# for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
#     j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
#     print j




################################ PLACES ###########################
# inputstr = "clinics"

# url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?%s' % urlencode((
#             ('input', inputstr),
#             ('inputtype', "textquery"),
#             ('key', api_key)
#  ))
# print url
# ur = urllib.urlopen(url)
# result = json.load(ur)

# print result


result = gmaps.places(location=(37.4419,-96.3413))
print result

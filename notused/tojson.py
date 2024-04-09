import json
import geocoder
from datetime import datetime
import car
from geopy.geocoders import Nominatim

carlist = [car("blank", "blank", "blank")]

def create(text, file):
    # add to database and add to session history
    g = geocoder.ip('me')
    date = str(datetime.now())

    dictionary = { text: {
        "Geolocation": {
            "Latitude": g.lat,
            "Longitude": g.lng
            },
        "Timestamp": date
        }
    }
    f = open("recognized.json", "w")
    file.update(dictionary)
    json.dump(file, f, indent=4)
    f.close()
    geolocator = Nominatim()
    location = geolocator.reverse(g.lat, g.lng)
    cab = car(text, location.address, date)
    carlist.append(cab)

def check(text):
    # checks to see if i've seen it today
    for x in carlist:
        # if i have then return
        if x.number == text:
            return
        
    # checks to see if i've seen it ever
    f = open("recognized.json", "r+")
    file = json.load(f)
    f.close()
    print(file.get(text))

    # if not then add to database
    if file.get(text) == None:
        create(text, file)
    # if i have seen it before but not today, then display and and to session history
    else:
        lat = file[text]["Geolocation"]["Latitude"]
        lng = file[text]["Geolocation"]["Longitude"]
        time = file[text]["Timestamp"]
        geolocator = Nominatim()
        location = geolocator.reverse(lat, lng)
        cab = car(text, location.address, time)
        cab.display()
        carlist.append(cab)
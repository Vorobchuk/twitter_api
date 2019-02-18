import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import ArcGIS



# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py
def name_loc(acct):
    """
    Return the dict of users and their locations
    :param acct: the name of user
    :return: dict,the key is user name and value is their location
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    #print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    #print(json.dumps(js, indent=2))

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    dic = {}
    for u in js['users']:
        #print(u['screen_name'])
        if ('location' not in u) or (u['location']==""):
            dic[u["screen_name"]] = " *No location found"
            continue
        else:
            dic[u["screen_name"]] = u["location"]
    return dic


def geo(location):
    """
    (str) -> list
    Returns the list of coordinates from locations
    :param location:
    :return: list of coordinates
    """
    geolocator = ArcGIS()
    try:
        location = geolocator.geocode(location, timeout=10)
        location = [location.latitude, location.longitude]

        return location
    except:
        pass


def map_create(dic):
    """
    (dict) -> None
    Builds the  html map with pointers. Pointers are the list of films.
    :param dic_m: the dictionary of locations and films
    :return: None
    """
    map = folium.Map()
    fg = folium.FeatureGroup(name="friend_location")
    for key, value in dic.items():
        try:
            if value != " *No location found":
                loc = geo(value)
                fg.add_child(folium.Marker(location=loc,
                                               popup=str(key).replace("'", ""),
                                               icon=folium.Icon()))
        except:
            continue

    map.add_child(fg)
    map.add_child(folium.LayerControl())
    return map.get_root().render()



def main(acct):
    map_create(name_loc(acct))


# acct = input("accaunt: ")
# main(acct)

import googlemaps
from pprint import pprint
from datetime import datetime

API = open('/Users/sophiakuo/Documents/23F-Python/Project/Code/gmap_api_config.txt', mode = 'r')
API_KEY = API.read()

def clean_origin(origin):
    cleaned_origin = origin.split(',') 
    cleaned_origin = "+".join(cleaned_origin)
    #print(cleaned_origin)
    return cleaned_origin


def get_journey(orgin, dest):
    myjourney = ()
    location = ()
    map_client = googlemaps.Client(key =  API_KEY)
    now = datetime.now()

    if dest == 'Target':
        location = (40.469564670226134, -79.92298646439406)
    elif dest == 'Aldi':
        location = (40.469779214761346, -79.93935154626831)
    else:
        location = (40.465339808542005, -79.91697031653943)

    direction_result = map_client.directions(orgin,location, mode="driving", avoid="ferries", departure_time=now, transit_mode = 'bus')

    dist = direction_result[0]['legs'][0]['distance']
    durat = direction_result[0]['legs'][0]['duration']
    myjourney = (dist['text'], durat['text'])
    return myjourney


def main(origin, dest):
    true_origin = clean_origin(origin)
    travel_stats = get_journey(true_origin, dest)
    print(travel_stats)
    return travel_stats


if __name__ == "__main__":
    main("4800,Forbes,Ave,Pittsburg,PA,15213",'Trader Joes' )
    
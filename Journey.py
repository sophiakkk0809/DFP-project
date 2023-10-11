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
    print(dist,'\n' , durat)
    myjourney = (dist['text'], durat['text'])
    return myjourney


def get_shortest_journey(orgin, dest):
    myjourney = ()
    location = ()
    map_client = googlemaps.Client(key =  API_KEY)
    now = datetime.now()

    target_location = {'Target East Liberty' : (40.469564670226134, -79.92298646439406)
    ,'Target Downtown' : (40.4398759,-79.9985603)
    , 'Target Waterfront': (40.4106088,-79.9107736)}

    aldi_location = {'ALDI Penn Avenue' : (40.46479415893555,-79.94145202636719)
    ,'Aldi Baum Boulevard' : (40.4582008,-79.9348865)
    ,'Aldi East Carson Street' : (40.4272488,-79.967989)
    ,'Aldi Butler Street' : (40.5111119,-79.9452459)
    ,'Aldi East 7th Avenue' : (40.4067341,-79.9123249)
    }

    tj_location = {'Trader Joe\'s Pittsburgh':(40.45899963378906,-79.91962432861328)
    ,'Trader Joe\'s Pittsburgh North Hills' : (40.549607,-80.043513)
    ,'Trader Joe\'s Pittsburgh - South Hills' : (40.3515402,-80.0517007)
    }

    temp_result = map_client.directions(orgin,(36.251240863991875,-114.920546637538), mode="driving", avoid="ferries", departure_time=now, transit_mode = 'bus')
    

    if dest == 'Target':
        for key,i in target_location.items():
            direction_result = map_client.directions(orgin,i, mode="driving", avoid="ferries", departure_time=now, transit_mode = 'bus')
            if direction_result[0]['legs'][0]['duration']['value']<temp_result[0]['legs'][0]['duration']['value']:
                temp_result = direction_result
                temp_store = key
        direction_result = temp_result
    elif dest == 'Aldi':
        for key,i in aldi_location.items():
            direction_result = map_client.directions(orgin,i, mode="driving", avoid="ferries", departure_time=now, transit_mode = 'bus')
            if direction_result[0]['legs'][0]['duration']['value']<temp_result[0]['legs'][0]['duration']['value']:
                temp_result = direction_result
                temp_store = key
        direction_result = temp_result
    else:
        for key,i in tj_location.items():
            direction_result = map_client.directions(orgin,i, mode="driving", avoid="ferries", departure_time=now, transit_mode = 'bus')
            if direction_result[0]['legs'][0]['duration']['value']<temp_result[0]['legs'][0]['duration']['value']:
                temp_result = direction_result
                temp_store = key
        direction_result = temp_result


    dist = direction_result[0]['legs'][0]['distance']
    durat = direction_result[0]['legs'][0]['duration']
    myjourney = (dist['text'], durat['text'],temp_store)
    return myjourney

def main(origin, dest):
    true_origin = clean_origin(origin)
    travel_stats = get_shortest_journey(true_origin, dest)
    print(travel_stats)
    return travel_stats


if __name__ == "__main__":
    main("4800,Forbes,Ave,Pittsburg,PA,15213",'Trader Joes' )
    
import requests
import csv,io
import json


def getKind(data):
    #print(data)
    if 'shops,squares,malls' in data:
          val= 'Shops,Squares,Malls'
    elif 'shops,malls,tourist_facilities' in data:
          val= 'Shops,Malls,Tourist facilities'
    elif 'bridges,architecture,interesting_places,other_bridges' in data:
          val= 'Bridges,Architecture'
    elif 'towers,architecture,interesting_places,other_towers'in data:
         val= 'Towers,Architecture'
    elif 'museums'in data:
           val= 'Museums,Cultural'

    elif 'skyscrapers,architecture,interesting_places'in data:
           val= 'Skyscrapers,Architecture'

    elif 'other_temples'in data:
           val= 'Religion,Buddhist Temple'
    elif  'buddhist_temples' in data:
           val= 'Religion,Buddhist Temple'
    elif 'churches'in data:
           val= 'Religion,Churches'
    elif 'mosques'in data:
           val= 'Religion,Mosque'

    elif 'hindu_temples'in data:
           val= 'Religion, Hindu Temple'
    elif 'other,unclassified_objects,interesting_places,tourist_object'in data:
           val='Other,Tourist'


    elif 'lighthouses,architecture,interesting_places'in data:
           val='Lighthouses'


    elif 'view_points,other,interesting_places'in data:
           val= 'Other'

    elif 'cinemas'in data:
           val='Cinemas'


    elif 'hotels'in data:
           val='Hotel'


    elif 'banks'in data:
           val='Banks'


    elif 'zoos'in data:
           val='Zoo'

    elif 'historic,monuments_and_memorials'in data:
           val='Historic,Monuments and Memorials'


    elif 'other_theatres'in data:
           val='Theatres'


    elif 'gardens_and_parks'in data:
           val= 'Gardens and Parks'

    else:
           val= 'Interesting places'

    return val

def getAttraction(opentripmap_api_key,radius,limit,offset,city_lon,city_lat):
    coordinates=[]
    location_dict={}
    attaction_res='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit={}&offset={}&lon={}&lat={}&rate=2'
    attaction_res=requests.get(attaction_res.format(opentripmap_api_key,radius,limit,offset,city_lon,city_lat)).json()
    for key in attaction_res['features']:
        value=key['properties']['kinds']
        name=key['properties']['name']
        coordinates.append(key["geometry"]['coordinates'])
        print(name)
        #location_dict.append(name)
        location_dict[key['properties']['name']]=[]
        message={'kind':getKind(value),'name':key['properties']['name'],"xid":key['properties']['xid']}
        location_dict[name].append(message)
        print(location_dict)
    context={
    "location_dict":location_dict,
    "coordinates":coordinates
    }
    return location_dict,coordinates

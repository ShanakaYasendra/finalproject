from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
import requests
import csv,io
import json


from .models import Country,CountryDetails,CountryCity

# Create your views here.
wetherApi='28719ed44bffb67e022e502067349ca0'
news_api_key='391409f008894221b310aec8d3d276d5'
opentripmap_api_key='5ae2e3f221c38a28845f05b6463508c4396871f980bf2a996c2306be'
offset=0
radius=0
city_lon= ''
city_lat=''

def index(request):
    try:
        county_all= Country.objects.all()
        context={
        'county_all':county_all}
    except Exception as e:

        context ={
        'county_all':'Can not find the Country'
        }
    return render(request,"Country/index.html",context)

def weather(request):
    lat = request.GET['Latitude']
    lon = request.GET['Longitude']
    url='https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&&units=metric&appid={}'
    wether_res= requests.get(url.format(lat,lon,wetherApi)).json()
    city_weather={
        'temperature':wether_res['main']['temp'],
        'description':wether_res['weather'][0]['description'],
        'icon':wether_res['weather'][0]['icon'],
    }

    return JsonResponse(city_weather)

def searchData(request):

    if request.method =='POST':
        try :
            searchVal = request.POST["searchVal"]
            country_Q= Country.objects.get(name=searchVal)
            countryDetails_q= CountryDetails.objects.get(countryId=country_Q.countryId)
            countryCity_q= CountryCity.objects.filter(countryName=searchVal)
            #print(countryCity_q)
        except Exception as e:
            print(e)
            county_all= Country.objects.all()
            context={
            "county_all": county_all,
            "messages":"Can Not Find The Country"
            }
            return render(request,"Country/index.html",context)
    country=country_Q.iso2Code
    #print(country)

    country_list=' http://api.worldbank.org/v2/country/{}?format=json'
    cr=requests.get(country_list.format(country)).json()
    #print(cr)
    con_pop_url='http://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?per_page=1&format=json'

    con_pop_res= requests.get(con_pop_url.format(country)).json()
    #print(con_pop_res)
    news_url='https://newsapi.org/v2/top-headlines?country={}&apiKey={}'
    news_response=requests.get(news_url.format(country,news_api_key)).json()
    #print(news_response)


    travel_url='https://www.travel-advisory.info/api?countrycode={}?format=json'
    travel_res=requests.get(travel_url.format(country)).json()


    country_de={
        #'region': cr[1]['incomeLevel']['value'],
        'name':country_Q.name,
        'region':country_Q.region,
        'iso2Code':country_Q.iso2Code,
        'latitude':countryDetails_q.latitude,
        'longitude':countryDetails_q.longitude,
        'capitalCity':countryDetails_q.capitalCity,
        'flag':country_Q.iso2Code.lower()
    }

    print(travel_res['data'][country]['advisory']['updated'])
    country_travel_advice={
    'score': travel_res['data'][country]['advisory']['score'],
    'updated':travel_res['data'][country]['advisory']['updated'],
    'source':travel_res['data'][country]['advisory']['source']


    }
    country_news={
        'total': news_response['totalResults'],
        'articles':news_response['articles'],
        'country':country_Q.name
    }
    context={
        #'city_weather': city_weather,
        'country_news':country_news,
        'country_population': con_pop_res,
        'country': country_de,
        'travel_advice':country_travel_advice,
        'city':countryCity_q

    }

    return render(request,'Country/resultPage.html',context)

def contact_upload(request):
    template='contact_upload.html'

    prompt={
        'order':'order shouldbe'
    }
    if request.method == "GET":
        return render(request, template,prompt)
    csv_file= request.FILES["file"]
    category=  request.POST.getlist('inputs')
    #print(category)
    #if not csv_file.name.endwith('.csv'):
       # message.error(request,"wrong file format")
    data_set =csv_file.read().decode('UTF-8')
    io_string =io.StringIO(data_set)
    next(io_string)
    if category[0]=='country':
        for colum in csv.reader(io_string, delimiter=',',quotechar='|'):
           _, created = Country.objects.update_or_create(

            countryId=colum[0],
            iso2Code=colum[1],
            name=colum[2],
            region=colum[3],
            regionIso=colum[4],
            regionValue= colum[5]
            )
        print(category)
    elif category[0]=='countryDetails':
        print('selection two')
        for colum in csv.reader(io_string, delimiter=',',quotechar='|'):
            _, created = CountryDetails.objects.update_or_create(

            countryId=colum[0],
            capitalCity= colum[1],
            longitude=colum[2],
            latitude= colum[3]

        )
    elif category[0]=='city':
        for colum in csv.reader(io_string, delimiter=',',quotechar='|'):
            _, created = CountryCity.objects.update_or_create(

            countryName= colum[0],
            city=colum[1],
            geonameid= colum[2]

        )
    context ={}
    return render(request, template, context)

def searchforAttraction(request):
    global offset
    global radius
    global city_lat
    global city_lon

    print('hello')

    if request.method =='POST':

        location=request.POST['city']
        radius=request.POST['radius']

        location_url="https://api.opentripmap.com/0.1/en/places/geoname?apikey={}&name={}&format=json"


        location_res=requests.get(location_url.format(opentripmap_api_key,location)).json()

        city_lon=location_res['lon']
        city_lat=location_res['lat']

        count_url='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset=0&lon={}&lat={}&rate=2&format=count&format=json'
        count_res=requests.get(count_url.format(opentripmap_api_key,radius,city_lon,city_lat)).json()
        attaction_res='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset={}&lon={}&lat={}&rate=2'
        attaction_res=requests.get(attaction_res.format(opentripmap_api_key,radius,offset,city_lon,city_lat)).json()

        coordinates=[]
        location_dict={}
        for key in attaction_res['features']:
            value=key['properties']['kinds']
            name=key['properties']['name']
            coordinates.append(key["geometry"]['coordinates'])
            #location_dict.append(name)
            location_dict[key['properties']['name']]=[]
            message={'kind':getKind(value),'name':key['properties']['name'],"xid":key['properties']['xid']}
            location_dict[name].append(message)


        print(coordinates)
        offset=0
        count=count_res
        context={
        'attraction':attaction_res,
        'count':count_res,
        'location':location_dict,
        'city':location,
        'city_lon':city_lon,
        'city_lat':city_lat,
        'coordinates':coordinates
        }

    return render(request,'location.html',context)


def loadtheList(request):
        global offset
        global radius
        global city_lat
        global city_lon
        offset+=5;
        print(city_lat)
        print(city_lon)
        attaction_res='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset={}&lon={}&lat={}&rate=2'
        attaction_res=requests.get(attaction_res.format(opentripmap_api_key,radius,offset,city_lon,city_lat)).json()
        return JsonResponse(attaction_res)

def attDeatils(request,xid):

    attraction_url='https://api.opentripmap.com/0.1/en/places/xid/{}?apikey={}&format=json'
    attraction_res=requests.get(attraction_url.format(xid,opentripmap_api_key)).json()

    image=attraction_res['preview']
    text= attraction_res['wikipedia_extracts']
    #name= attraction_res['wikipedia_extracts']

    #print(attraction_res)
    attraction={
    'preview':image,
    'wikipedia_extracts':text,
    #'name':name
    }

    context={
    'attraction':attraction

    }
    return JsonResponse(attraction)

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
           val= 'interesting places'

    return val

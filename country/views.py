from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
import requests
import csv,io
import json


from .models import Country,CountryDetails,CountryCity
from . import uploadutils
from . import util
# Create your views here.
wetherApi='28719ed44bffb67e022e502067349ca0'
news_api_key='391409f008894221b310aec8d3d276d5'
opentripmap_api_key='5ae2e3f221c38a28845f05b6463508c4396871f980bf2a996c2306be'
offset=0
radius=0
 
city_lat  = None
city_lon = None
country=None

# Main page loading this will return the country list from the model
def index(request):
    global country,offset,radius,city_lat,city_lon
    
    offset=0
    radius=0
    city_lon= None
    city_lat=None
    country=None
    try:

        county_all= Country.objects.all()
        context={
        'county_all':county_all}
    except Exception as e:

        context ={
        'county_all':'Can not find the Country'
        }
    return render(request,"Country/index.html",context)

# This view returns the Weather of the current user location as a Json
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

# dailywether view return the next 7 days weather forcast
def dailyweather(lat,lon):

    url='https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely,current&&units=metric&appid={}'
    daily_res=requests.get(url.format(lat,lon,wetherApi)).json()
    #print(daily_res)
    return daily_res

#Return the coutry detailsis base on the search input from the main page and pass the data to results page
#use model query for country, country detais and city details
def searchData(request):
    global country,city_lat,city_lon
    city_lat  = None
    city_lon = None
    if request.method =='POST':
        try :
            searchVal = request.POST["searchVal"]
            country=searchVal
            country_Q= Country.objects.get(name=searchVal)
            countryDetails_q= CountryDetails.objects.get(countryId=country_Q.countryId)
            countryCity_q= CountryCity.objects.filter(countryName=searchVal).order_by('city')
            countryiso=country_Q.iso2Code
            #print(countryCity_q)
        except Exception as e:
            #print(e)
            county_all= Country.objects.all()
            context={
            "county_all": county_all,
            "messages":"Can Not Find The Country"
            }
            return render(request,"Country/index.html",context)
    else:
        #print(country)
        try :
            #searchVal = request.POST["searchVal"]
            #county=searchVal
            country_Q= Country.objects.get(name=country)
            countryDetails_q= CountryDetails.objects.get(countryId=country_Q.countryId)
            countryCity_q= CountryCity.objects.filter(countryName=country).order_by('city')
            print(countryCity_q)
            countryiso=country_Q.iso2Code
        except Exception as e:
            print(e)
            county_all= Country.objects.all()
            context={
            "county_all": county_all,
            "messages":"Can Not Find The Country"
            }
            return render(request,"Country/index.html",context)

    
    #print(countryiso)
    try:
        country_list=' http://api.worldbank.org/v2/country/{}?format=json'
        cr=requests.get(country_list.format(countryiso)).json()
        #print(cr)
        con_pop_url='http://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?per_page=1&format=json'

        con_pop_res= requests.get(con_pop_url.format(countryiso)).json()
        #print(con_pop_res)
        news_url='https://newsapi.org/v2/top-headlines?country={}&apiKey={}'
        news_response=requests.get(news_url.format(countryiso,news_api_key)).json()
        #print(news_response['articles'])


        travel_url='https://www.travel-advisory.info/api?countrycode={}?format=json'
        travel_res=requests.get(travel_url.format(countryiso)).json()


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

        #print(travel_res['data'][country]['advisory']['updated'])
        country_travel_advice={
        'score': travel_res['data'][countryiso]['advisory']['score'],
        'updated':travel_res['data'][countryiso]['advisory']['updated'],
        'source':travel_res['data'][countryiso]['advisory']['source']


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
    except Exception as e:
        message="Something is Wrong Please Click Home"
        #print(e)
        context={
            "message":message
        }
        return render(request, "Error.html",context)


#Admin function  wich allow superusers to upload the data to the Country tables
def contact_upload(request):
    template='contact_upload.html'
    prompt={
        'order':'Please Select the Upload'
    }

    if request.user.is_superuser:

        if request.method == "GET":
            return render(request, template,prompt)
        csv_file= request.FILES["file"]
        category=  request.POST.getlist('inputs')


        #print(csv_file.endswith('.csv'))

        if not csv_file.name.endswith(".csv"):
             message= "wrong file format"
             context={
                 "message": message
             }
             return render(request,template,context)

        elif category !=[]:
            if category[0]=='country':
               #print(category)
               message= uploadutils.upload_country(csv_file)

        #return render(request,template,context)

            elif category[0]=='countryDetails':
                #print(category)
                message= uploadutils.upload_details(csv_file)

        #return render(request,template,context)


            elif category[0]=='city':
                message= uploadutils.upload_city(csv_file)

            else:
                message= "nothing to upload"


            context={
                "message":message
                }
            return render(request, template, context)
        else:
            message= "Please select the category to upload"
            context={
                "message":message
                }
            return render(request, template, context)

# Return the data for search city and the search radius
def searchforAttraction(request):
    global offset
    global radius
    global city_lat
    global city_lon
    global country
    #offset = None
    #city_lat  = None
    #city_lon = None
    
    #print('hello')
    try:
        if request.method =='POST':

            location=request.POST['city']
            radius=request.POST['radius']
            #countryCity_q= CountryCity.objects.filter(countryName=country).order_by('city')
            location_url="https://api.opentripmap.com/0.1/en/places/geoname?apikey={}&name={}&format=json"


            location_res=requests.get(location_url.format(opentripmap_api_key,location)).json()

            city_lon=location_res['lon']
            city_lat=location_res['lat']

            daily_weather=dailyweather(city_lat,city_lon)
            count_url='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset=0&lon={}&lat={}&rate=2&format=count&format=json'
            count_res=requests.get(count_url.format(opentripmap_api_key,radius,city_lon,city_lat)).json()
            attaction_res='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset={}&lon={}&lat={}&rate=2'
            attaction_res=requests.get(attaction_res.format(opentripmap_api_key,radius,offset,city_lon,city_lat)).json()

            coordinates=[]
            location_dict={}
            location_dict,coordinates=util.getAttraction(opentripmap_api_key,radius,5,offset,city_lon,city_lat)


            if len(location_dict)<5:
                dif= 5-len(location_dict)
                limit=10
                coordinates.clear()
                #location_dict.clear()
                location_dict,coordinates=util.getAttraction(opentripmap_api_key,radius,limit,offset,city_lon,city_lat)

            else:
                offset=0



            #print(location_dict)

            count=count_res
            context={
            #'attraction':attaction_res,
            'count':count_res,
            'location':location_dict,
            'city':location,
            'city_lon':city_lon,
            'city_lat':city_lat,
            'coordinates':coordinates,
            'daily_Weather':daily_weather,
            #'cityies':countryCity_q

            }

        return render(request,'Country/location.html',context)

    except Exception as e:
        message="Something is Wrong Please Click Home"
        #print(e)
        context={
            "message":message
        }
        return render(request, "Error.html",context)



# this will retrun data to next page list
def loadtheList(request):
        global offset
        global radius
        global city_lat
        global city_lon
        offset+=5;
        #print(city_lat)
        #print(city_lon)
        try:
            attaction_res='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset={}&lon={}&lat={}&rate=2'
            attaction_res=requests.get(attaction_res.format(opentripmap_api_key,radius,offset,city_lon,city_lat)).json()
            #print(attaction_res)
            return JsonResponse(attaction_res)
        except Exception as e:
            message="Something is Wrong Please Click Home"
            #print(e)
            context={
                "message":message
            }
            return render(request, "Error.html",context)

# Make the API call to bring the data for attarction
def attDeatils(request,xid):
    try:
        attraction_url='https://api.opentripmap.com/0.1/en/places/xid/{}?apikey={}&format=json'
        attraction_res=requests.get(attraction_url.format(xid,opentripmap_api_key)).json()
        try:
            image=attraction_res['preview']
        except Exception as e:
            image=""
        try:
            text= attraction_res['wikipedia_extracts']
        except Exception as e:
            text=""

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
    except Exception as e:
        message="Something is Wrong Please Click Home"
        #print(e)
        context={
            "message":message
        }
        return render(request, "Error.html",context)

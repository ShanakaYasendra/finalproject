from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
import requests
import csv,io


from .models import Country,CountryDetails,CountryCity

# Create your views here.
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
    return render(request,"weather/index.html",context)

def process_loc(request):
    lat = float(request.GET.get('lat'))
    lon = float(request.GET.get('lon'))
    #print('lat')

    url='https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&&units=metric&appid=28719ed44bffb67e022e502067349ca0'
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=28719ed44bffb67e022e502067349ca0'

    wether_res= requests.get(url.format(lat,lon)).json()
    #print(wether_res)
    city_weather={
        'temperature':wether_res['main']['temp'],
        'description':wether_res['weather'][0]['description'],
        'icon':wether_res['weather'][0]['icon'],
    }
    print(wether_res['main']['temp'])
    context={
    'city_weather': city_weather,
    }
    return render(request,'weather/index.html',context)

def searchData(request):

    if request.method =='POST':
        try :
            searchVal = request.POST["searchVal"]

            print(searchVal)
            country_Q= Country.objects.get(name=searchVal)
            #country_filter =Country.objects.filter(name=searchVal.capitalize())| Country.objects.filter(countryId=searchVal.upper())
            #print(country_list.name)

            countryDetails_q= CountryDetails.objects.get(countryId=country_Q.countryId)
            countryCity_q= CountryCity.objects.filter(countryName=searchVal)
            print(countryCity_q)
        except Exception as e:
            print(e)
            county_all= Country.objects.all()
            context={
            "county_all": county_all,
            "messages":"Can Not Find The Country"
            }
            return render(request,"weather/index.html",context)
    country=country_Q.iso2Code
    print(country)


    country_list=' http://api.worldbank.org/v2/country/{}?format=json'
    cr=requests.get(country_list.format(country)).json()
    #print(cr)
    con_pop_url='http://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?per_page=1&format=json'

    con_pop_res= requests.get(con_pop_url.format(country)).json()
    #print(con_pop_res)
    news_url='https://newsapi.org/v2/top-headlines?country={}&apiKey={}'
    #'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=391409f008894221b310aec8d3d276d5'
    #https://newsapi.org/v2/top-headlines?country=us&apiKey=391409f008894221b310aec8d3d276d5
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



    #city_weather={
    #    'city':city,
    #    'temperature':r['main']['temp'],
    #    'description':r['weather'][0]['description'],
    #    'icon':r['weather'][0]['icon'],


    #}
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

    return render(request,'weather/resultPage.html',context)

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
        #location='colombo'
        #print(location)
        location_url="https://api.opentripmap.com/0.1/en/places/geoname?apikey={}&name={}&format=json"


        location_res=requests.get(location_url.format(opentripmap_api_key,location)).json()
        #print(location_res['lat'])
        #print(location_res['lon'])
        city_lon=location_res['lon']
        city_lat=location_res['lat']

        count_url='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset=0&lon={}&lat={}&rate=2&format=count&format=json'
        count_res=requests.get(count_url.format(opentripmap_api_key,radius,city_lon,city_lat)).json()
        #'https://api.opentripmap.com/0.1/en/places/radius?apikey=5ae2e3f221c38a28845f05b6463508c4396871f980bf2a996c2306be&radius={}000&limit=5&offset=0&lon=79.84868&lat=6.93548&rate=2&format=count'
        #print(count_res)
        attaction_url='https://api.opentripmap.com/0.1/en/places/radius?apikey=5ae2e3f221c38a28845f05b6463508c4396871f980bf2a996c2306be&radius=1&limit=5&offset=0&lon={}&lat={}&rate=2&format=json'
        attaction_res='https://api.opentripmap.com/0.1/en/places/radius?apikey={}&radius={}000&limit=5&offset={}&lon={}&lat={}&rate=2'
        attaction_res=requests.get(attaction_res.format(opentripmap_api_key,radius,offset,city_lon,city_lat)).json()
        print(attaction_res)
        offset=0
        context={
        'attraction':attaction_res,
        'count':count_res
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
        context={
        'attraction':attaction_res,
        }
        print(attaction_res)
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
def getGeoname(geodata):

    return geoType,catagory

from django.shortcuts import render
from django.http import HttpResponse
import requests
import csv,io


from .models import Country
# Create your views here.


def index(request):
    return render(request,"weather/index.html")
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

def resultpage(request):
    country='us'

    #url='https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&&units=metric&appid=28719ed44bffb67e022e502067349ca0'
    city= 'Melbourne, AU'
    r= requests.get(url.format(city)).json()
    #print(r)

    country_list=' http://api.worldbank.org/v2/country/{}?format=json'
    cr=requests.get(country_list.format(country)).json()
    #print(cr)
    con_pop_url='http://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?per_page=1&format=json'

    con_pop_res= requests.get(con_pop_url.format(country)).json()
    #print(con_pop_res)
    news_url='https://newsapi.org/v2/top-headlines?country={}&apiKey=391409f008894221b310aec8d3d276d5'
    #'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=391409f008894221b310aec8d3d276d5'
    #https://newsapi.org/v2/top-headlines?country=us&apiKey=391409f008894221b310aec8d3d276d5
    news_response=requests.get(news_url.format(country)).json()
    #print(news_response)

    travel_url='https://www.travel-advisory.info/api?countrycode={}?format=json'
    travel_res=requests.get(travel_url.format(country)).json()
    #print(travel_res)

    country_de={
        'region': cr[1],
        #'latitude':cr[1]['latitude']
    }



    #city_weather={
    #    'city':city,
    #    'temperature':r['main']['temp'],
    #    'description':r['weather'][0]['description'],
    #    'icon':r['weather'][0]['icon'],


    #}
    country_travel_advice={

    }
    country_news={
        'total': news_response['totalResults'],
        'articles':news_response['articles']
    }
    context={
        #'city_weather': city_weather,
        'country_news':country_news,
        'country_population': con_pop_res,
        'country': country_de,
        'travel_advice':travel_res

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
    #if not csv_file.name.endwith('.csv'):
       # message.error(request,"wrong file format")
    data_set =csv_file.read().decode('UTF-8')
    io_string =io.StringIO(data_set)
    next(io_string)

    for colum in csv.reader(io_string, delimiter=',',quotechar='|'):
        _, created = Country.objects.update_or_create(
            countryId=colum[0],
            iso2Code=colum[1],
            name=colum[2],
            region=colum[3],
            regionIso=colum[4],
            regionValue= colum[5],
            capitalCity= colum[6],
            longitude=colum[7],
            latitude= colum[8]

        )
    context ={}
    return render(request, template, context)
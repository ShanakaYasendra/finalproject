from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):
    country='us'
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=28719ed44bffb67e022e502067349ca0'
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
    print(travel_res)

    country_de={
        'region': cr[1],
        #'latitude':cr[1]['latitude']
    }

   
    
    city_weather={
        'city':city,
        'temperature':r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon'],


    }
    country_travel_advice={

    }
    country_news={
        'total': news_response['totalResults'],
        'articles':news_response['articles']
    }
    context={
        'city_weather': city_weather,
        'country_news':country_news,
        'country_population': con_pop_res,
        'country': country_de,
        'travel_advice':travel_res

    }
   
    return render(request,'weather/index.html',context)
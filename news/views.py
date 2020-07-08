from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):
    country='AU'
    url='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=28719ed44bffb67e022e502067349ca0'
    city= 'Melbourne, AU'
    r= requests.get(url.format(city)).json()
    #print(r)

    cov_url='https://covid-19.dataflowkit.com/v1/:{}'
    #'https://covid-19.dataflowkit.com/v1'
    #'https://localcoviddata.com/covid19/v1/cases/eucdc?country=AU&daysInPast=4'
    #
    cov_res= requests.get(cov_url.format(country)).json()

    news_url='https://newsapi.org/v2/top-headlines?country={}&apiKey=391409f008894221b310aec8d3d276d5'
    #'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=391409f008894221b310aec8d3d276d5'
    #https://newsapi.org/v2/top-headlines?country=us&apiKey=391409f008894221b310aec8d3d276d5
    news_response=requests.get(news_url.format(country)).json()
    print(news_response)

    
    city_weather={
        'city':city,
        'temperature':r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon'],


    }
    country_news={
        'total': news_response['totalResults'],
        'articles':news_response['articles']
    }
    context={
        'city_weather': city_weather,
        'country_news':country_news,
        'cov_res':cov_res
    }
    #geodata = response.json()
    #return render(request, 'core/home.html', {
       # 'ip': geodata['ip'],
       # 'country': geodata['country_name']
    return render(request,'weather/index.html',context)
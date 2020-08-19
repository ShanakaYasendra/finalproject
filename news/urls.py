from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchData',views.searchData,name='searchData'),
    path('weather', views.weather, name='weather'),
    path('attraction',views.searchforAttraction, name='attraction'),
    path('attDeatils/<str:xid>', views.attDeatils,name='attDeatils'),
    path('listload', views.loadtheList, name='listload'),
    path('upload-csv',views.contact_upload, name="contact_upload")
]

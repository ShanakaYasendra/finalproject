from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchData',views.searchData,name='searchData'),
    path('process_loc', views.process_loc, name='process_loc'),
    path('attraction',views.searchforAttraction, name='attraction'),
    path('upload-csv',views.contact_upload, name="contact_upload")
]

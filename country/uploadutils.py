import csv,io
from .models import Country,CountryDetails,CountryCity
def upload_county(csv_file):
    try:
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
            regionValue= colum[5]
            )
        message= "Upload Successfull"
    except Exception:
        message = "Something went wrong Nothing Uploaded"
    return message

def upload_details(csv_file):
    try:
        data_set =csv_file.read().decode('UTF-8')
        io_string =io.StringIO(data_set)
        next(io_string)
        for colum in csv.reader(io_string, delimiter=',',quotechar='|'):
            _, created = CountryDetails.objects.update_or_create(

            countryId=colum[0],
            capitalCity= colum[1],
            longitude=colum[2],
            latitude= colum[3]

        )
        message= "Upload Successfull"
    except Exception:
        message = "Something went wrong Nothing Uploaded"
    return message
def upload_city(csv_file):
    try:
        data_set =csv_file.read().decode('UTF-8')
        io_string =io.StringIO(data_set)
        next(io_string)
        for colum in csv.reader(io_string, delimiter=',',quotechar='|'):
            _, created = CountryCity.objects.update_or_create(

            countryName= colum[0],
            city=colum[1],
            geonameid= colum[2]

        )
        message= "Upload Successfull"
    except Exception:
        message = "Something went wrong Nothing Uploaded"
    return message

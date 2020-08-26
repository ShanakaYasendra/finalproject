import csv
import os
from xml.etree import ElementTree


os.chdir("/Users/shan/Development/mysite/finalproject/news/static")
tree= ElementTree.parse("country.xml")


# open a file for writing

Resident_data = open('/Users/shan/Development/mysite/finalproject/news/static/ResidentData.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(Resident_data)
resident_head = []

count = 0
for member in root.findall('Resident'):
	resident = []
	address_list = []
	if count == 0:
		name = member.find('country').tag
		resident_head.append(country)
		PhoneNumber = member.find('name').tag
		resident_head.append(name)
		EmailAddress = member.find('iso2Code').tag
		resident_head.append(iso2Code)
		
		csvwriter.writerow(resident_head)
		count = count + 1

	name = member.find('name').text
	resident.append(name)
	PhoneNumber = member.find('iso2Code').text
	resident.append(PhoneNumber)
	
	csvwriter.writerow(resident)
Resident_data.close()

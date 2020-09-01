# final project

# Explore the World
Web app is mainly focus on providing information about the country.
  - Travel warning
  - NEWS
  - Next Seven days Weather forecast
  - City Attraction
  - Country details
App is develop using
  - Django framework
  - JavaScript
  - CSS
  - HTML
  - bootstrap

# Index.html

This is the landing or Home Page.
when user visit the page, it will map the local location and display the current time and weather on top.
JavaScript use to get the weather and times
Search input load the country dropdown user can type or select from the list.
  - Country list load from the Country Model.
  - Data is collect from **worldbank**.




# resultPage.html

This will bring the data for the Search query from the index page.

Display Country details, county capital mark in the Map, Country Flag.
Information gather using **world bank API**.

Display news for the country using **News API**.

Model dialog use to enter city and the radius to display the attraction.

Leaf map use to display maps in the page.
JavaScript use with marking the location in the map.

# locationPage.html

Display attraction base on the city search. 5 records per_page and location map in the Leaf map. this use Javascript.

When user click on the list item it will display the information about the attraction.this use **opentripmap api**.

top of the page display next 7 days forecast using **openweathermap api**.

JavaScript and Ajax use with next button to load the next list without refreshing the page.

# layout.HTML
main layout page design using html.

# main.css
All the page style and media queries define in this Page

# main.Js
All the JavaScript function are implement using main.js

# contact_upload.html
 this is an Admin page. To use This user, need to be super user.
 Allows to upload data from csv files to Django models
  - Country
  - city
  - Country details

# Util.py
 Function use by the view is define in the util.py.

# uploadutils.py
Unload relate functions define in the uploadutils.py.

# models.py

Following tables define in the models.py
  - Country
  - city
  - Country details
# views.py
all the backend calls define using views.

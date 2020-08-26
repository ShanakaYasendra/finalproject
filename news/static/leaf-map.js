// See post: http://asmaloney.com/2014/01/code/creating-an-interactive-map-with-leaflet-and-openstreetmap/
var city_lon={{city_lon}}
var city_lat={{city_lat}}
var map = L.map( 'poi', {
  center: [20.0, 5.0],
  minZoom: 2,
  zoom: 2
}).setView([city_lat, city_lon], 12);

L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  subdomains: ['a', 'b', 'c']
}).addTo( map )

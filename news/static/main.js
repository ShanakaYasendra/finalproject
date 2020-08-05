

function onloadfun(){
  getLocation();
  startTime();
}


function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();

    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('clock').innerHTML =
    h + ":" + m + ":" + s;

    var t = setTimeout(startTime, 500);
  }
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }
  //var x = document.getElementById("demo");
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  var spanlo= document.getElementById('getLocation');
  var Latitude= position.coords.latitude ;
  spanlo.setAttribute("Latitude",Latitude);
console.log(Latitude);

var Longitude= position.coords.longitude;
spanlo.setAttribute("Longitude",Longitude);
console.log("la is" +Longitude);

$.ajax({
            type: "GET",
            url: 'https://api.openweathermap.org/data/2.5/weather?lat='+Latitude+'&lon='+Longitude+'&&units=metric&appid=28719ed44bffb67e022e502067349ca0',

            //contentType: "application/json",
        dataType: 'json',

            success : function(data) {
          console.log(data);
               document.getElementById('getLocation').innerHTML+=data.main.temp;
            var img=   document.createElement('img')
            var src=data.weather[0].icon;
            img.setAttribute("src","https://openweathermap.org/img/w/"+src+".png")
            var imgLoc= document.getElementById('image');
            imgLoc.appendChild(img)
           }
         }

)}

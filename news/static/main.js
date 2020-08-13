

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

            var img=   document.createElement('img')
            var src=data.weather[0].icon;
            img.setAttribute("src","https://openweathermap.org/img/w/"+src+".png")
            var imgLoc= document.getElementById('image');


          let mainpageDiv=document.getElementById('weather');
          let ptag= document.createElement('p');
          //var celcius= &#8451;
          ptag.innerHTML+=data.main.temp;
          if( typeof(mainpageDiv) !='undefined' && mainpageDiv != null)
          {
              mainpageDiv.appendChild(img);
              mainpageDiv.appendChild(ptag);
          }
          else {
                imgLoc.appendChild(img)
                 document.getElementById('getLocation').innerHTML+=data.main.temp;
          }





           }
         }

)}


function showDetails(xid){
 console.log(xid);
  $.ajax({

    url:'/attDeatils/'+xid,
     dataType: 'json',
    success : function(data) {
               console.log('request Success')
               //var img={{data.attraction.image}};
               onShowPOI(data);
           }

  })
}

function onShowPOI(data) {
      let poi = document.getElementById("poi");
      poi.innerHTML = "";
      //let image= document.createElement('img');
      //image.setAttribute("src",data.image);
      //image.setAttribute("width",'300px');
      //image.setAttribute("hight",'300px');
      //poi.appendChild(image);
      if (data.preview) {
        poi.innerHTML += `<img src="${data.preview.source}">`;
      }
      poi.innerHTML += data.wikipedia_extracts
        ? data.wikipedia_extracts.html
        : data.info
       ? data.info.descr
        : "No description";

      //poi.innerHTML += `<p><a target="_blank" href="${data.otm}">Show more at OpenTripMap</a></p>`;
    }

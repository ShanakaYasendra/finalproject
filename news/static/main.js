
let offset=0;
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
          var celcius=Math.round(data.main.temp);
          ptag.innerHTML+=celcius+'&#8451;';
          if( typeof(mainpageDiv) !='undefined' && mainpageDiv != null)
          {
              //ptag.innerHTML+=data.main.temp+'&#8451;';
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
  function loadlist(){

    $.ajax({

      url:'/listload',
       dataType: 'json',
      success : function(data) {
                 console.log('request Success');
                 redrawtheList(data)
                 //var img={{data.attraction.image}};
                 //onShowPOI(data);
             }

    })
}
function redrawtheList(data){
  let listdata=document.getElementById('listdata');
  listdata.innerHTML="";
  let list = document.createElement("div");
      list.setAttribute("id","list")
       list.innerHTML = "";
       console.log('hi')

       data.features.forEach(item => list.appendChild(createListItem(item)));
       listdata.appendChild(list);
     }
function createListItem(item) {
         let a = document.createElement("a");
         a.className = "list-group-item list-group-item-action";
         a.setAttribute("data-id", item.properties.xid);
         a.innerHTML = `<h5 class="list-group-item-heading">${item.properties.name}</h5>
                   <p class="list-group-item-text">${item.properties.kinds}</p>`;

         a.addEventListener("click", function() {
           document.querySelectorAll("#list a").forEach(function(item) {
             item.classList.remove("active");
           });
           this.classList.add("active");
           let xid = this.getAttribute("data-id");
           showDetails(xid).then(data => onShowPOI(data));
         });
         return a;
       }

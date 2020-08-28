
let offset=0;
function onloadfun(){
  getLocation();
  startTime();
}

///Set the local time
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
    if (i < 10) {i = "0" + i};
    return i;
  }
///Return local Location for Wether
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

///Setting the Local weather for index page and Navigation Bar
function showPosition(position) {
  var spanlo= document.getElementById('getLocation');
  var Latitude= position.coords.latitude ;
  spanlo.setAttribute("Latitude",Latitude);
console.log(Latitude);

var Longitude= position.coords.longitude;
spanlo.setAttribute("Longitude",Longitude);
console.log("la is" +Longitude);
data={
  'Longitude':Longitude,
  'Latitude':Latitude
}
$.ajax({
            'type': "GET",

            'url': '/weather',
            'data':data,


            success : function(data) {
        //  console.log(data);

            var img=   document.createElement('img')
            var src=data.icon;
            img.setAttribute("src","https://openweathermap.org/img/w/"+src+".png")
            var imgLoc= document.getElementById('image');


          let mainpageDiv=document.getElementById('weather');
          let ptag= document.createElement('p');
          var celcius=Math.round(data.temperature);
          ptag.innerHTML+=celcius+'&#8451;';

          if( typeof(mainpageDiv) !='undefined' && mainpageDiv != null)
          {
              ptag.innerHTML+='<br>'+'Current Wether in your Area' + data.description;
              mainpageDiv.appendChild(img);
              mainpageDiv.appendChild(ptag);
          }
          else {
                imgLoc.appendChild(img)
                 document.getElementById('getLocation').append(ptag);
          }





           }
         }

)}

///Draw the first list of the attraction
function loadFirstList(){
  $.ajax({

    url:'/attraction',
     dataType: 'json',
    success : function(data) {
               //console.log('request Success');
               redrawtheList(data)

           }

  })
}

/// Setting the Attraction Details in the POI div area
///request the API called to VIEW
function showDetails(xid){
 console.log(xid);
  $.ajax({

    url:'/attDeatils/'+xid,
     dataType: 'json',
    success : function(data) {
               onShowPOI(data);
           }

  })
}

///Setting the respose data from VIew and load on the page without refresh

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
  }

/// Clear the POI div data and request the newxt 5 Items for the list
///called by next button
function loadlist(){
    let poi = document.getElementById("poi");
    poi.innerHTML = "";
    $.ajax({

      url:'/listload',
       dataType: 'json',
      success : function(data) {
                 console.log('request Success');
                 redrawtheList(data);
                 drawMap(data);

                 //var img={{data.attraction.image}};
                 //onShowPOI(data);
             }

    })
}

///Load the data for the next page list items
function redrawtheList(data){
  let listdata=document.getElementById('listdata');
  listdata.innerHTML="";
  let list = document.createElement("div");
      list.setAttribute("id","list")
       list.innerHTML = "";


       data.features.forEach(item => list.appendChild(createListItem(item)));
       listdata.appendChild(list);


     }
function createListItem(item) {
         let a = document.createElement("a");
         a.className = "list-group-item list-group-item-action";
         a.setAttribute("data-id", item.properties.xid);
         a.innerHTML = `<h5 class="list-group-item-heading">${item.properties.name}</h5>
                   <p class="list-group-item-text">${getGeoName(item.properties.kinds)}</p>`;

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

/// Draw the Map and mark the attarction on the next page list
  function drawMap(item)
  {
    mymap.remove();
    mymap = L.map( 'poi', {
      center: [20.0, 5.0],
      minZoom: 2,
      zoom: 2
    }).setView([city_lat, city_lon], 15);

     L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',

    }).addTo( mymap )

    for (var i = 0; i < item.features.length; i++) {
        let a=item.features[i].geometry.coordinates[0];
        let b= item.features[i].geometry.coordinates[1];
              L.marker([b,a])
              .bindPopup(item.features[i].properties.name)
                  .addTo(mymap);
          }
     //L.marker([city_lat, city_lon]).addTo(mymap);
  }

/// Return the Attraction Kind
function getGeoName(item){
  if (item.includes('shops,squares,malls')){
    return 'Shops,Squares,Malls'
  }
  else if (item.includes('shops,malls,tourist_facilities')) {
    return 'Shops,Malls,Tourist facilities'

  }
  else if (item.includes('bridges,architecture,interesting_places,other_bridges')) {
    return 'Bridges,Architecture'

  }

else if (item.includes('towers,architecture,interesting_places,other_towers')) {

  return 'Towers,Architecture'
}
else if (item.includes('museums')) {

  return 'Museums,Cultural'
}
else if (item.includes('skyscrapers,architecture,interesting_places')) {

  return 'Skyscrapers,Architecture'
}
else if ((item.includes('religion,other_temples'))||(item.includes('religion,buddhist_temples')) ){
  return 'Religion,Buddhist Temple'

}
else if (item.includes('religion,churches')) {
  return 'Religion,Churches'

}
else if (item.includes('religion,mosques')) {
  return 'Religion,Mosque'

}
else if (item.includes('religion,hindu_temples')) {
  return 'Religion,Temple'

}
else if (item.includes('other,unclassified_objects,interesting_places,tourist_object')) {
  return'Other,Tourist'

}
else if (item.includes('lighthouses,architecture,interesting_places')) {
  return 'Lighthouses'

}
else if (item.includes('view_points,other,interesting_places')) {
  return 'Other'
}
else if (item.includes('cinemas')) {
  return'Cinemas'

}
else if (item.includes('hotels')) {
  return'Hotel'

}
else if (item.includes('banks')) {
  return'Banks'

}
else if (item.includes('zoos')) {
  return 'Zoo'
}
else if (item.includes('historic,monuments_and_memorials')) {
  return'Historic,Monuments and Memorials'

}
else if (item.includes('other_theatres')) {
  return'Theatres'

}
else if (item.includes('gardens_and_parks')) {
  return 'Gardens and Parks'
}
else{
  return 'Interesting places'
}
}

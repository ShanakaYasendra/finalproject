
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
    if (i < 10) {i = "0" + i};
    return i;
  }

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
data={
  'Longitude':Longitude,
  'Latitude':Latitude
}
$.ajax({
            'type': "GET",

            'url': '/weather',
            'data':data,


            success : function(data) {
          console.log(data);

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
              ptag.innerHTML+='<br>'+data.description.toUpperCase();
              mainpageDiv.appendChild(img);
              mainpageDiv.appendChild(ptag);
          }
          else {
                imgLoc.appendChild(img)
                 document.getElementById('getLocation').innerHTML+=data.temperature;
          }





           }
         }

)}
function loadFirstList(){
  $.ajax({

    url:'/attraction',
     dataType: 'json',
    success : function(data) {
               console.log('request Success');
               redrawtheList(data)
               //var img={{data.attraction.image}};
               //onShowPOI(data);
           }

  })
}

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
    let poi = document.getElementById("poi");
    poi.innerHTML = "";
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
  return 'interesting places'
}
}

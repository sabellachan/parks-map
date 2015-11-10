var parkIcon = 'static/img/tree-yellowicon.png';
var visitedIcon = 'static/img/tree-greenicon.png';

function initMap() {

  var startLatLng = new google.maps.LatLng(38.705, -121.169);

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: startLatLng,
    scrollwheel: false,
    zoom: 7,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    styles: [
      {"stylers": [
          {"hue": "#bbff00"},
          {"weight": 0.5},
          {"gamma": 0.5}
        ]
      },
      {"elementType": "labels",
       "stylers": [
          {"visibility": "off"}
        ]
      },
      {"featureType": "landscape.natural",
       "stylers": [
          {"color": "#a4cc48"}
        ]
      },
      {"featureType": "road",
       "elementType": "geometry",
       "stylers": [
          {"color": "#ffffff"},
          {"visibility": "on"},
          {"weight": 1}
        ]
      },
      {"featureType": "administrative",
       "elementType": "labels",
       "stylers": [
          {"visibility": "on"}
        ]
      },
      {"featureType": "road.highway",
       "elementType": "labels",
       "stylers": [
          {"visibility": "simplified"},
          {"gamma": 1.14},
          {"saturation": -18}
        ]
      },
      {"featureType": "road.highway.controlled_access",
       "elementType": "labels",
       "stylers": [
          {"saturation": 30},
          {"gamma": 0.76}
        ]
      },
      {"featureType": "road.local",
       "stylers": [
          {"visibility": "simplified"},
          {"weight": 0.4},
          {"lightness": -8}
        ]
      },
      {"featureType": "water",
       "stylers": [
          {"color": "#4aaecc"}
        ]
      },
      {"featureType": "landscape.man_made",
       "stylers": [
          {"color": "#718e32"}
        ]
      },
      {"featureType": "poi.business",
       "stylers": [
          {"saturation": 68},
          {"lightness": -61}
        ]
      },
      {"featureType": "administrative.locality",
       "elementType": "labels.text.stroke",
       "stylers": [
          {"weight": 2.7},
          {"color": "#f4f9e8"}
        ]
      },
      {"featureType": "road.highway.controlled_access",
       "elementType": "geometry.stroke",
       "stylers": [
          {"weight": 1.5},
          {"color": "#e53013"},
          {"saturation": -42},
          {"lightness": 28}
        ]
      }
    ],
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });


  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, getBounds());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, getBounds());
  }

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}

  var infoWindow = new google.maps.InfoWindow({
      width: 150
  });

  // Get the HTML input element for the autocomplete search box.
  var input = document.getElementById('search');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Create the autocomplete object.
  var autocomplete = new google.maps.places.Autocomplete(input);

  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    var place = autocomplete.getPlace();
    if (place.geometry) {
       map.panTo(place.geometry.location);
       map.setZoom(8);
    }
  });

  // Retrieving the information with AJAX
    $.get('/parks.json', function (parks) {

        var parksArray = parks.parks;

        var park, marker, html;

        for (var i = 0; i < parksArray.length; i++) {
            park = parksArray[i];

            // Define the marker
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(park.recAreaLat, park.recAreaLong),
                map: map,
                icon: parkIcon,
                id: park.recAreaID,
                draggable: false,
                title: 'Rec Area ' + park.recAreaName,
            });

            // Define the content of the infoWindow
            html = (
                '<div class="window-content">' +
                    '<p><b>ID: </b>' + park.recAreaID + '</p>' +
                    '<p><b>Name: </b>' + park.recAreaName + '</p>' +
                    '<p><b>Description: </b>' + park.recAreaDescription + '</p>' +
                    '<p><b>Activities: </b>' + park.recAreaActivities + '</p>' +
                    '<p><b>Phone Number: </b>' + park.recAreaPhoneNumber + '</p>' +
                    '<form id="visited-park" action=\'/add-park\' method=\'POST\'>' +
                    '<input type="hidden" name="park-name" id="park-id" value="'+ park.recAreaID +'">' +
                    '<input id="visit-button" type="submit" value="I\'ve visited this park">' + '<p><div id="msg"></div></p>' +
                    '</form>' +
                '</div>');


            bindInfoWindow(marker, map, infoWindow, html);
        }
    });

   $.get('/parks-visited.json', function (parks) {

      var parksArray = parks.parks;

      var park, marker, html;

      for (var i = 0; i < parksArray.length; i++) {
          park = parksArray[i];

          // Define the marker
          marker = new google.maps.Marker({
              position: new google.maps.LatLng(park.recAreaLat, park.recAreaLong),
              map: map,
              icon: visitedIcon,
              id: park.recAreaID,
              draggable: false,
              title: 'Rec Area ' + park.recAreaName,
          });

          // Define the content of the infoWindow
          html = (
              '<div class="window-content">' +
                  '<p><b>ID: </b>' + park.recAreaID + '</p>' +
                  '<p><b>Name: </b>' + park.recAreaName + '</p>' +
                  '<p><b>Description: </b>' + park.recAreaDescription + '</p>' +
                  '<p><b>Activities: </b>' + park.recAreaActivities + '</p>' +
                  '<p><b>Phone Number: </b>' + park.recAreaPhoneNumber + '</p>' +
                  '<form id="visited-park" action=\'/add-park\' method=\'POST\'>' +
                  '<input type="hidden" name="park-name" id="park-id" value="'+ park.recAreaID +'">' +
                  '<input id="visit-button" type="submit" value="I haven\'t been to this park"><div id="msg"></div>' +
                  '</form>' +
              '</div>');

          bindInfoWindow(marker, map, infoWindow, html);
      }
  });

  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
            $("#visited-park").on("submit", function(evt) {
            evt.preventDefault();
            $.post('/add-park', {"park-id": $('#park-id').val()}, function(msg){
              $("#msg").empty().append(msg);
              changeIcon(marker);
              changeText();
              }); // post park-id value
            });  // on submit
      }); // click listener after infoWindow exists
  } // close bindInfoWindow

  function changeIcon(marker) {
    if (marker.icon === parkIcon) {
      marker.setIcon(visitedIcon);
    } else {
      marker.setIcon(parkIcon);
    }
  } // close changeIcon

  function changeText() {
    var buttonText = document.getElementById("visit-button");
      if (buttonText.value=="I\'ve visited this park") buttonText.value = "I haven\'t been to this park";
      else buttonText.value = "I\'ve visited this park";
  } //close changeText
  
} // close init function

google.maps.event.addDomListener(window, 'load', initMap);


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
    {
    "featureType": "administrative",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "off"
        }
    ]
    },
    {
    "featureType": "administrative",
    "elementType": "geometry.stroke",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "administrative",
    "elementType": "labels",
    "stylers": [
        {
            "visibility": "on"
        },
        {
            "color": "#716464"
        },
        {
            "weight": "0.01"
        }
    ]
    },
    {
    "featureType": "administrative.country",
    "elementType": "labels",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "landscape",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "landscape.natural",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "landscape.natural.landcover",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi",
    "elementType": "geometry.fill",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi",
    "elementType": "geometry.stroke",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi",
    "elementType": "labels.text",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi",
    "elementType": "labels.text.stroke",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "poi.attraction",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "road",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "road.highway",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "off"
        }
    ]
    },
    {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "road.highway",
    "elementType": "geometry.fill",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "road.highway",
    "elementType": "geometry.stroke",
    "stylers": [
        {
            "visibility": "simplified"
        },
        {
            "color": "#a05519"
        },
        {
            "saturation": "-13"
        }
    ]
    },
    {
    "featureType": "road.local",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "transit",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "transit",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "simplified"
        }
    ]
    },
    {
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "water",
    "elementType": "all",
    "stylers": [
        {
            "visibility": "simplified"
        },
        {
            "color": "#84afa3"
        },
        {
            "lightness": 52
        }
    ]
    },
    {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
        {
            "visibility": "on"
        }
    ]
    },
    {
    "featureType": "water",
    "elementType": "geometry.fill",
    "stylers": [
        {
            "visibility": "on"
        }
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
  $.get('/parks.json', function(data){
    passParksInformation(data, parkIcon, "I\'ve visited this park");
  });

  $.get('/parks-visited.json', function(data){
    passParksInformation(data, visitedIcon, "I haven\'t been to this park");
  });

  function passParksInformation(parks, icon, message) {
        var parksArray = parks.parks;

        var park, marker, html;

        for (var i = 0; i < parksArray.length; i++) {
            park = parksArray[i];

            // Define the marker
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(park.recAreaLat, park.recAreaLong),
                map: map,
                icon: icon,
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
                    '<input id="visit-button" type="submit" value="'+ message +'">' + '<p><div id="msg"></div></p>' +
                    '</form>' +
                '</div>');

            bindInfoWindow(marker, map, infoWindow, html);
        }
    }
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


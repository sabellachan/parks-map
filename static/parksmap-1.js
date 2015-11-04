function initMap() {

  var startLatLng = new google.maps.LatLng(38.705, -121.169);

  var bounds = new google.maps.LatLngBounds();

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: startLatLng,
    bounds: bounds,
    scrollwheel: false,
    zoom: 7,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
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

  google.maps.event.addListener(map, 'bounds_changed', getParksInfo);

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}

  var infoWindow = new google.maps.InfoWindow({
      width: 150
  });

function getParksInfo() {
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
                draggable: false,
                title: 'Rec Area ' + park.recAreaName,
            });

            // Define the content of the infoWindow
            html = (
                '<div class="window-content">' +
                    '<p><b>ID: </b>' + park.recAreaID + '</p>' +
                    '<p><b>Name: </b>' + park.recAreaName + '</p>' +
                    '<p><b>Description: </b>' + park.recAreaDescription + '</p>' +
                    '<p><b>Phone Number: </b>' + park.recAreaPhoneNumber + '</p>' +
                    '<form action=\'/add-park\' method=\'POST\'>' +
                    '<input type="hidden" name="park-name" value="'+ park.recAreaID +'">' +
                    '<input type="submit" id="visited-park" value="I\'ve visited this park">' +
                    '</form>' +
                '</div>');

            bindInfoWindow(marker, map, infoWindow, html);
        }

    });
}

  function bindInfoWindow(marker, map, infoWindow, html, recAreaID, userID) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }
}

google.maps.event.addDomListener(window, 'load', initMap);
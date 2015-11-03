function initMap() {

  var myLatLng = {lat: 38.705, lng: -121.169};

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    scrollwheel: false,
    zoom: 7,
    zoomControl: false,
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
      handleLocationError(true, infoWindow, map.getBounds());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getBounds());
  }

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}

  var infoWindow = new google.maps.InfoWindow({
      width: 200
  });

  google.maps.event.bounds_changed;

  // Retrieving the information with AJAX
  $.get('/parks.json', function (parks) {

      var parks_array = parks.parks;

      var park, marker, html;

      for (var i = 0; i < parks_array.length; i++) {
          park = parks_array[i];

          // Define the marker
          marker = new google.maps.Marker({
              position: new google.maps.LatLng(park.recAreaLat, park.recAreaLong),
              map: map,
              title: 'Rec Area ' + park.recAreaName,
          });

          // Define the content of the infoWindow
          html = (
              '<div class="window-content">' +
                  '<p><b>Name: </b>' + park.recAreaName + '</p>' +
                  '<p><b>Description: </b>' + park.recAreaDescription + '</p>' +
                  '<p><b>Phone Number: </b>' + park.recAreaPhoneNumber + '</p>' +
                  '<p><b>Reservation URL: </b>' + park.recAreaReservation + '</p>' +
              '</div>');

          bindInfoWindow(marker, map, infoWindow, html);
      }

  });

  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }
}

google.maps.event.addDomListener(window, 'load', initMap);

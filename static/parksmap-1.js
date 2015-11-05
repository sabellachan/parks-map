var markersArray = [];

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

  // Set the default bounds for the autocomplete search results.
  // This will bias the search results to North America.
  var defaultBounds = new google.maps.LatLngBounds(
    new google.maps.LatLng(27, 133),
    new google.maps.LatLng(72, 40));

  var options = {
    bounds: defaultBounds
  };

  // Get the HTML input element for the autocomplete search box.
  var input = document.getElementById('search');
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Create the autocomplete object.
  var autocomplete = new google.maps.places.Autocomplete(input, options);

function getParksInfo() {
  // // remove any old markers
  //   for (var i=0; i < markersArray.length; i++){
  //     markersArray[i].setMap(null);
  //   }
  //   markersArray.length = 0;


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
                    '<p><b>Activities: </b>' + park.recAreaActivities + '</p>' +
                    '<p><b>Phone Number: </b>' + park.recAreaPhoneNumber + '</p>' +
                    '<form id="visited-park" action=\'/add-park\' method=\'POST\'>' +
                    '<input type="hidden" name="park-name" id="park-id" value="'+ park.recAreaID +'">' +
                    '<input type="submit" value="I\'ve visited this park">' +
                    '</form>' +
                '</div>');


            // markersArray.push(marker);
            bindInfoWindow(marker, map, infoWindow, html);
        }

    });
}

  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);

          infoWindow.open(map, marker);
      });
  }
  google.maps.event.addListener(infoWindow, 'domready', function() {
              $("#visited-park").on("submit", function(evt) {
                  evt.preventDefault();
                  console.log("hi!");
                    $.post('/add-park', {"park-id": $('#park-id').val()}, function(msg){
                      console.log(msg);
                    });
              });  // on submit
  }); // bind listener after infoWindow exists

}

google.maps.event.addDomListener(window, 'load', initMap);


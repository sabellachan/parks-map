function initMap() {

  // Specify where the map is centered
  var myLatLng = {lat: 72, lng: -140};

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
      center: myLatLng,
      zoom: 5,
      mapTypeControl: true,
      zoomControl: true,
      mapTypeId: google.maps.MapTypeId.TERRAIN
  });


// $.get('/parks.json', function (parks) {
//     var park, marker, html;

//     for (var key in parks) {
//       park = parks[key];

//       marker = new google.maps.Marker({
//         position: new google.maps.LatLng(park)
//         map: map,
//         title: 'Rec Area: ' + park.recAreaName
//       });

//       html = (
//         '<div class="window-content">' +
//             '<p><b>Description: </b>' + park.recAreaDescription + '</p>' +
//             '<p><b>Contact Phone Number: </b>' + park.recAreaPhoneNumber + '</p>' +
//             '<p><b>Reservation URL: </b>' + park.recAreaReservation + '</p>' +
//         '</div>');

//       bindInfoWindow(marker, map, infoWindow, html);
//     }
// });

var infoWindow = new google.maps.InfoWindow({
      width: 300,
      content: 'Test'
  });

var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Rec Area'
  });

  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });
}

function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }



google.maps.event.addDomListener(window, 'load', initMap);
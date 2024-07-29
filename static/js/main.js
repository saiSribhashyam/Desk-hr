function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), 
    {
        zoom: 3,
        //Create London's UK longitude and latitude for location maps
        center: {
            lat: 51.509865,
            lng: -0.118092
        }
    });

    // Create an array of alphabetical characters used to label the markers.
    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    //Create South East & East London's longitude and latitude for location maps
    const locations = [
          { lat: 51.507465, lng: 0.127809 },
          { lat: 51.483465, lng: 0.058692 },
    ];

    // Add some markers to the map.
    const markers = locations.map((position, i) => {
        const label = labels[i % labels.length];
        const marker = new google.maps.Marker({
          position,
          label,
        });

         // open info window when marker is clicked
        marker.addListener("click", () => {
          infoWindow.setContent(label);
          infoWindow.open(map, marker);
        });
  
        return marker;
    });
  
    // Add a marker clusterer to manage the markers.
    new markerClusterer.MarkerClusterer({ markers, map });
}


document.addEventListener("DOMContentLoaded", function() {

  // Dismisses messages alert after 5 seconds

    $('.alert').delay(5000).fadeOut(1000);
});


// Back to top button
  // Create toggle
  window.onscroll = () => {
        toggleTopButton();
  };
  
  // When user scrolls down 20px from the top of the page, display button
  function toggleTopButton() {
      if (document.body.scrollTop > 20 ||
          document.documentElement.scrollTop > 20) {
        document.getElementById('back-to-up').classList.remove('d-none');
      } else {
        document.getElementById('back-to-up').classList.add('d-none');
      }
  }


// Updates footer's copyright year with the current year
  const year = document.querySelector('#current-year');
  year.innerHTML = new Date().getFullYear();
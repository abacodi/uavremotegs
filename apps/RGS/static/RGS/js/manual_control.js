$(document).ready(function() {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Function to update the UAV's state every second
    // Initialize the map
    var mymap = L.map('mapid').setView([lat, lon], 30); // center the map to some default coordinates, these should be replaced by your UAV's starting coordinates
    
    // Add a tile layer to the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 30,
    }).addTo(mymap);
    
    // Create a new line (polyline) instance. This will hold the path of your UAV.
    var polyline = L.polyline([], {color: 'red'}).addTo(mymap);
    
    function updateState(){
        // AJAX call
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'update_data'},
            success: function(data) {
                // Update the UAV state indicators as before
                $('#is_armed').text(data.is_armed);
                $('#altitude').text(data.altitude);
                $('#velocity').text(data.velocity);
                $('#location').text(data.location);
    
                // Now update the map
                var lat = data.location[0];
                var lon = data.location[1];
                mymap.setView([lat, lon], 15); // re-center the map to the UAV's current location
                polyline.addLatLng([lat, lon]); // add the new point to the polyline
            },
        });
    };
    
    // Start the periodic state update
    setInterval(updateState, 1000); // update every second

    // Set event handlers for the buttons
    $('.btn-info').click(function(){
        var id = this.id;
        var direction = id.replace('btnMove', '').toLowerCase();

        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: direction},
        });
    });

    $('#btnUpdate').click(function(){
        updateState();
    });

    $('#btnTakeOff').click(function(e){
        e.preventDefault();
        var altitude = $('#takeOffAltitude').val();

        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'take_off', altitude: altitude},
            success: function(data) {
                alert('Drone taking off..')
            },
        });
    });

    $('#btnLand').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'land_drone'},
            success: function(data) {
                alert('Drone landing..')
            },
        });
    });

    /* POST SAFE METHOD */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

});

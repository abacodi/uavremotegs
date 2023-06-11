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
                $('#altdata').text(data.altitude);
                $('#velocity').text(data.velocity);
                $('#location').text(data.location);
    
                // Now update the map
                var lat = data.location[0];
                var lon = data.location[1];
                mymap.setView([lat, lon],16); // re-center the map to the UAV's current location
                polyline.addLatLng([lat, lon]); // add the new point to the polyline
            },
        });
    };

    // Update state every second
    setInterval(updateState, 1000);

    // Add marker to the map
    function addMarker(lat, lon) {
        var marker = L.marker([lat, lon]).addTo(mymap);
    }

    mymap.on('click', function(e) {
        var latitude = e.latlng.lat;
        var longitude = e.latlng.lng;
        var altitude = 20;

        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'add_waypoint', latitude: latitude, longitude: longitude, altitude: altitude},
            success: function(data) {
                // Add row to the table
                $('#waypointsTable').append('<tr><td>' + latitude + '</td><td>' + longitude + '</td><td>' + altitude + '</td></tr>');
                // Add marker to the map
                addMarker(latitude, longitude);
            },
        });
    });
    
    // add waypoint
    $('#waypointForm').submit(function(e){
        e.preventDefault();
        var latitude = $('#latitude').val();
        var longitude = $('#longitude').val();
        var altitude = $('#altitude').val();

        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'add_waypoint', latitude: latitude, longitude: longitude, altitude: altitude},
            success: function(data) {
                $('#waypointsTable').append('<tr><td>' + latitude + '</td><td>' + longitude + '</td><td>' + altitude + '</td></tr>');
                // Add marker to the map
                addMarker(latitude, longitude);
            },
        });
    });

    // start mission
    $('#btnStartMission').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'start_mission'},
            success: function(data) {
                alert('Mission started');
            },
        });
    });

    // end mission
    $('#btnEndMission').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'end_mission'},
            success: function(data) {
                alert('Mission ended');
            },
        });
    });

    $('#addWaypoint').click(function(){
        var latitude = $('#latitude').val();
        var longitude = $('#longitude').val();
        var altitude = $('#altitude').val();

        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'add_waypoint', latitude: latitude, longitude: longitude, altitude: altitude},
            success: function(data) {
                // Clear the table
                $('#table').find('tr:gt(0)').remove();

                // Re-populate the table
                data.waypoints.forEach(function(waypoint) {
                    $('#waypointsTable').append('<tr><td>' + latitude + '</td><td>' + longitude + '</td><td>' + altitude + '</td></tr>');
                    // Add marker to the map
                    addMarker(latitude, longitude);
                });

            },
        });
    });

    /* POST SAFE METHOD */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

});

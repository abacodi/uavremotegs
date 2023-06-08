$(document).ready(function() {
    
    // Function to update the UAV's state every second
    function updateState(){
        // Then, send also the data of the projects hours
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        // AJAX call
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'update_data'},
            success: function(data) {
                $('#is_armed').text(data.is_armed);
                $('#altitude').text(data.altitude);
                $('#velocity').text(data.velocity);
            },
        });
    };
    // Call the function to start
    updateState();   


    // Function to update the UAV's state every second
    function armVehicle(){
        // Then, send also the data of the projects hours
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        // AJAX call
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'arm_uav'},
            success: function(data) {
                $('#is_armed').text(data.is_armed);
                $('#altitude').text(data.altitude);
                $('#velocity').text(data.velocity);
                alert('UAV ARMED')
            },
        });
    };

    $('#btnArm').click(function(){
        armVehicle();
    });

    $('#btnUpdate').click(function(){
        updateState();
    });

    $('#btnMoveNorth').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: 'north'},
        });
    });
    
    $('#btnMoveSouth').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: 'south'},
        });
    });
    
    $('#btnMoveEast').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: 'east'},
        });
    });
    
    $('#btnMoveWest').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: 'west'},
        });
    });
    
    $('#btnMoveUp').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: 'up'},
        });
    });
    
    $('#btnMoveDown').click(function(){
        $.ajax({
            method: "POST",
            url: window.location.href,
            data: {trigger: 'move_drone', direction: 'down'},
        });
    });

    /* POST SAFE METHOD */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

});

$(document).ready(function() {
    function refreshDashboardData(){
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
            data: {trigger: 'update_telemetry'},
            success: function(data) {
                $('#altitude').text(data.altitude);
                $('#location').text(data.location);
                $('#heading').text(data.heading);
                $('#velocity').text(data.velocity);
                $('#battery').text(data.battery);
                $('#mode').text(data.mode);
                $('#is_armed').text(data.is_armed);
                
                // For updating config parameters
                let configList = $('#paramconfTable').empty();
                for(let key in data.config) {
                    configList.append(`<tr><th>${key}:</th> <th>${data.config[key]}</th></tr>`);
                }
                $("#paramconfTable tr").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf($("#paramFilter").val()) > -1)
                });
            },
            complete: function(data) {
                // Schedule the next request when this one's complete
                setTimeout(refreshDashboardData, 1000); // The number is in milliseconds, so 1000 means 1 seconds
            }
        });
    };
    // Call the function to start
    refreshDashboardData();
    $("#paramFilter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#paramconfTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    /* POST SAFE METHOD */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

});

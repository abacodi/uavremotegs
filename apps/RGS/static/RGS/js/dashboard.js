$(document).ready(function() {
    function refreshDashboardData() {
        $.ajax({
            url: '/dashboard/',
            type: 'GET',
            success: function(data) {
                // Update the page with the new data
                $('#altitude').text(data.altitude);
                $('#location').text(data.location);
                $('#heading').text(data.heading);
                $('#velocity').text(data.velocity);
                $('#battery').text(data.battery);
                $('#mode').text(data.mode);
                $('#is_armed').text(data.is_armed);
                
                // For updating config parameters
                let configList = $('#config').empty();
                for(let key in data.config) {
                    configList.append(`<li><strong>${key}:</strong> ${data.config[key]}</li>`);
                }
            },
            complete: function(data) {
                // Schedule the next request when this one's complete
                setTimeout(refreshDashboardData, 5000); // The number is in milliseconds, so 5000 means 5 seconds
            }
        });
    };
    // Call the function to start
    refreshDashboardData();
});

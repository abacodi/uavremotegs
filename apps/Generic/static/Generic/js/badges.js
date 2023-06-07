$(document).ready(function (){
    // Change the database
    seen_all();

    // Function to update all badges as seeen
    function seen_all(){
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
            data: {trigger: 'update_seen'},
            success: function(data) {
                console.log("updated database");
            }
        });
    };

    /* POST SAFE METHOD */
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
});
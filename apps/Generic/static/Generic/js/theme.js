$(document).ready(function () {


    let theme=JSON.parse(json_theme);
    let theme_value = theme;

    if (theme != ""){
        let row = $('#row'+theme);
        var value = theme;
        row.children('.cell').css('background-color', 'var(--active-bg-color)');

    }

    $('tr').click(function(event) {
        console.log("click")
        $('.cell').css('background-color', 'var(--bg-color)');
        $(this).children('.cell').css('background-color', 'var(--active-bg-color)');
        value = parseInt(this.id.replace("row",""));
        console.log(value)
        $('#id_theme_value').val(value);
    }).mouseover(function(event) {
        $(this).css('border','2px solid black');
        $(this).css('cursor', 'pointer' );
    }).mouseleave(function(){
        $(this).css('border','1px solid black');
    });

    $('#submit_theme').click(function update_theme(){
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
            data: {trigger: 'new_theme', theme_id : value},
            success: function(data) {
                console.log(data.msg);
                window.location.href = "";
                // 
            }
        });
    });


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

});
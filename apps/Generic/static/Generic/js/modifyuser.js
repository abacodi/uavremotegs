$(document).ready(function () {
    window.removeEventListener
    let user = selected_user;

    $("#user-dropdown-menu").change( function () {
        user = document.getElementById('user-dropdown-menu').value
        reload_data(user);
    });

    $('#div_id_password1')[0].style.display="none";
    $('#div_id_password2')[0].style.display="none";
    document.getElementById("id_password2").setAttribute('value','Kaskdljaoisdj123!');
    document.getElementById("id_password1").setAttribute('value','Kaskdljaoisdj123!');

    function reload_data(user){
        var new_address=window.location.href;
        var n = new_address.indexOf('modifyuser/');
        new_address=new_address.substring(0, n+11);
        new_address=new_address + user;
        window.location.href=new_address;

    };

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };
});
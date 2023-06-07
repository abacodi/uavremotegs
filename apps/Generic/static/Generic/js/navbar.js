$(window).resize(function () {
    if ($('#navBar').width()<=1200){
        $('#ringIcon').css("margin-left","10px");
        $('#ringIcon').css("margin-right","10px");
        $('.btn-outline-success').css("margin-left","10px");

    }
    else {
        $('#ringIcon').css("margin-left","0px");
        $('#ringIcon').css("margin-right","0px");
        $('.btn-outline-success').css("margin-left","0px");
    }
});

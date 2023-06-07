$(document).ready(function () {

    $('#button_add_op').appendTo('#footermodal_mod');
    $('#close_mod').appendTo('#footermodal_mod');
    
    if(reload == 'True'){
        window.location.href = window.location.href;
    };
    if(email_sent == 'True'){
        $('#succes_modal').modal();
    };
    if(change_site == 'True'){
        var new_address=window.location.href;
        var n = new_address.indexOf('internal_op/');
        new_address=new_address.substring(0, n+12);
        new_address=new_address + new_id;
        window.location.href=new_address;
    };

    tinymce.init({
        selector: '#email_description',
        plugins: 'anchor autolink charmap codesample emoticons link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tinycomments tableofcontents footnotes mergetags autocorrect',
        toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
        tinycomments_mode: 'embedded',
        branding: false
    });

    tinymce.init({
        selector: '#id_description',
        plugins: 'anchor autolink charmap codesample emoticons link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tinycomments tableofcontents footnotes mergetags autocorrect',
        toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | addcomment showcomments | spellcheckdialog a11ycheck | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
        tinycomments_mode: 'embedded',
        branding: false
    });

    /* POST METHOD */
   function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
   }


});
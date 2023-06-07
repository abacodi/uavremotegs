// function resize() {
//
//         //    resize the wrapper in HOME
//         // var h = window.innerHeight-80;
//         // var txt =  h + "px";
//         // document.getElementById("wrapper").style.height = txt;
//
//
//
// };

function tablesize() {
    var a = $('#div_table_container > div > div.react-grid-Main > div > div.react-grid-Header > div > div').width();
    var b = $('.react-grid-HeaderRow').width();
    var c = $('#div_table_container').width();

    $('.react-grid-Container').width(c);
    $('.react-grid-Canvas').width(c);
    $('.react-grid-HeaderRow').width(c-10);

    if ( a < c){
         $('.react-grid-Container').width(a);
         $('.react-grid-Canvas').width(a);
         $('.react-grid-HeaderRow').width(a-10);
    }else{
        // $('.react-grid-Container').width($('#content').width()-30);
        // $('.react-grid-Canvas').width($('#content').width()-30);
        // $('.react-grid-HeaderRow').width($('#content').width()-40);
    }

}
 $(window).resize(function() {
     $('.box').height($('body').height());
         var h = $('.box').height() - $('#navBar').height() - $('#contentFooter').height();
    $('#wrapper').height(h);
    var width = $('#wrapper').width() - $('.sidebar-content').width();
    $('#content').css('max-width','none');
    $('#content').width(width);

   tablesize();

 });

$(document).ready(function () {

    $('.box').height($('body').height());

    // Initial size of wrapper in HOME
    var h = $('.box').height() - $('#navBar').height() - $('#contentFooter').height();
    $('#wrapper').height(h);

    // Initial width of the container
    var width = $('#wrapper').width() - $('.sidebar-content').width();
    $('#content').css('max-width','none');
    $('#content').width(width);


    tablesize();


    setTimeout(function () {
        tablesize();
    },10);

    // Initial size of the jumbotron's container
    let cont_jumbos=document.getElementsByClassName('cont_jumbo')
    if(cont_jumbos.length>0){
        var id = document.getElementsByClassName('cont_jumbo')[0].id;

        $('#jumbo_news').height($('#head_news').height()+$('#cont_news').height()+$('#checkbox_jumbo').height()+150);
        $('#jumbo_descr').height($('#head_descr').height()+$('#cont_descr').height()+60);
        $('#jumbo_his').height($('#head_history').height()+$('#cont_history').height()+60);

        // Heights of jumbotrons to compare
        let h_jumbo_news = 0;
        let h_jumbo_his = 0;
        let h_jumbo_descr = 0;
        if($('#jumbo_news').height()!==undefined){
            h_jumbo_news = $('#jumbo_news').height();
        }
        if($('#jumbo_his').height()!==undefined){
            h_jumbo_his = $('#jumbo_his').height();
        } 
        if($('#jumbo_descr').height()!==undefined){
            h_jumbo_his = $('#jumbo_descr').height();
        }

        // greater height of jumbotrons
        var jumbo_height = Math.max(h_jumbo_descr,h_jumbo_his,h_jumbo_news);
        $('.jumbotron').height(jumbo_height);
    }

    var h3 = $('#module').height() - $('.nav-pills').height() - 41 - $('#tabs_home').height() - 90;
    $('#container_home').height(h3);
});



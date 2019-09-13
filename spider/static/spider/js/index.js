$(document).ready(function() {
    $( "#crawlerForm" ).submit(function( event ) {
        event.preventDefault();
        var $form = $( this );
        var url = $form.find( "input[id='url']" ).val();
        var depth = $form.find( "input[id='depth']" ).val();
        var post_url = $form.attr( "action" );
        console.log(url);
        console.log(depth);
        console.log(post_url);

        $.post( post_url, { url: url, depth: depth }, function( data ) {
            console.log( data.pagesToVisit );
        }, "json");
    });
});
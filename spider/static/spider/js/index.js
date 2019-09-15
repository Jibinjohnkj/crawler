$(document).ready(function() {
    var getLinks = "/spider/get-links/";
    var getImages = "/spider/get-images/";

    $( "#crawlerForm" ).submit(function( event ) {
        event.preventDefault();

        var $form = $( this );
        var url = $form.find( "input[id='url']" ).val();
        var depth = $form.find( "input[id='depth']" ).val();

        console.log(url);
        console.log(depth);

        $("#error").hide();
        $("#submitButton").css("display", "none");
        $("#loadingButton").css("display", "block");
        $("#searchResults").empty();

        $.get( getLinks, { url: url, depth: depth })
            .done(function( data ) {
                console.log(data.links);
                for(var i = 0; i < data.links.length; i++) {
                    if (i==0){
                        // for first link, insert images and scroll
                        $.ajax({
                            async: false,
                            method: "GET",
                            url: getImages,
                            data: { url: data.links[i]}
                        })
                        .done(function( response ) {
                            console.log(response.url);
                            injectGallery(response.url, response.images);
                            $("html, body").animate({ scrollTop: $(document).height() }, 1500);
                          })
                        .always(function() {
                            $("#loadingButton").css("display", "none");
                            $("#submitButton").css("display", "block");
                         });

                    }
                    else{
                        $.get( getImages, { url: data.links[i]}, function( response ) {
                            injectGallery(response.url, response.images);
                        });
                    }

                }
          })
            .fail(function() {
                $("#error").show();
                $("#loadingButton").css("display", "none");
                $("#submitButton").css("display", "block");
            });

    });

    function injectGallery(url, images ) {
        //For each link, populate and insert images
        var linkTmpl = $.templates("#linkTemplate");
        var linkData = {link:url};
        var linkHtml = linkTmpl.render(linkData);
        var imagesHtml = '';
        for(var i = 0; i < images.length; i++) {
            var imageTmpl = $.templates("#imageTemplate");
            var imageData = {image:images[i]};
            var imageHtml = imageTmpl.render(imageData);
            imagesHtml += imageHtml;
        }
        $("#searchResults").append(linkHtml+'<div class="gallery" id="gallery">'+imagesHtml+'</div>');
    }


});
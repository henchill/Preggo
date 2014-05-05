$(document).ready(function () {
    //Modal Function
    var modal = (function(){
        var 
        method = {},
        $overlay,
        $modal,
        $modalContent,
        $close;

        // Append the HTML
        $overlay = $('<div id="overlay"></div>');
        $modal = $('<div id="modal"></div>');
        $modalContent = $('<div id="content"></div>');
        $close = $('<a id="close" href="#">close</a>');

        $modal.hide();
        $overlay.hide();
        $modal.append($modalContent, $close);

        $(document).ready(function(){
            $('body').append($overlay, $modal);
        });

        // Center the modal in the viewport
        method.center = function () {
            var top, left;

            top = Math.max($(window).height() - $modal.outerHeight(), 0) / 2;
            left = Math.max($(window).width() - $modal.outerWidth(), 0) / 2;

            $modal.css({
                top:top + $(window).scrollTop(), 
                left:left + $(window).scrollLeft()
            });
        };

        // Open the modal
        method.open = function (settings) {
            $modalContent.empty().append(settings.modalContent);

            $modal.css({
                width: settings.width || 'auto', 
                height: settings.height || 'auto'
            })

            method.center();

            $(window).bind('resize.modal', method.center);

            $modal.show();
            $overlay.show();
        };

        // Close the modal
        method.close = function () {
            $modal.hide();
            $overlay.hide();
            $modalContent.empty();
            $(window).unbind('resize.modal');
        };

        $close.click(function(e){
            e.preventDefault();
            method.close();
        });

        return method;
    }());

	$(".clickable").click(function(evt) {        
        modal.open({modalContent: "<p>Howdy my name is sim sima</p><br>"});
        console.log("clicked");
    });
});

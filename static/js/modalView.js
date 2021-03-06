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
        $overlay = $("#overlay");//$('<div id="overlay"></div>');
        $modal = $("#modal"); //$('<div id="modal"></div>');
        $modalContent = $("#content"); //$('<div id="content"></div>');
        $close = $("#close"); //$('<a id="close" href="#"><img src="static/media/Images/close.png></a>');

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

            // $modal.css({
            //     width: settings.width || 'auto', 
            //     height: settings.height || 'auto'
            // })

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
        var postid = $(this).attr("data-post-id");
        $.get("/preggo/view_post/", {post_id: postid}, 
            function(data) {
                modal.open({modalContent: data});
            }
        );
    });

        
    $("#new-post").click(function(event) {
        $.get("/preggo/add_post/", {}, 
            function(data) {
                modal.open({modalContent: data});
            }
        );
    });
    
//     $("#post_form").submit(function(event) {
//         event.preventDefault();
//         var form = $(this);
//         var url = form.attr('action');
//         $.post(url, {}, function(data) {
//             modal.close();
//         });
//     });
        
        
        
});

$(document).ready(function () {
    // Updates upvotes for questions
    $('.quest-upvotes').each(function () {
        $(this).click(function(){        

            var questid;
            questid = $(this).attr("data-quest-id");  
            $.get('/preggo/upvote_question/', {question_id: questid},                                        
                function(data, status){
                var selector = "#quest-upvotes-count-" + questid;  
                console.log(data);                              
                $(selector).html(data);
            });
                            
        });
    });    
    
    // Updates downvotes for questions
    $('.quest-downvotes').each(function () {
        $(this).click(function(){            
            var questid;
            questid = $(this).attr("data-quest-id");  
            $.get('/preggo/downvote_question/', {question_id: questid},                                           function(data, status){
                var selector = "#quest-downvotes-count-" + questid;                                
                $(selector).html(data);
            });
                            
        });
    });  
    
    // Updates upvotes for posts
    $('.post-upvotes').each(function () {
        $(this).click(function(){            
            var postid;
            console.log("upvoted");
            postid = $(this).attr("data-post-id");  
            $.get('/preggo/upvote_post/', {post_id: postid},                                           function(data, status){
                var selector = "#post-upvotes-count-" + postid;                                
                $(selector).html(data);
            });
                            
        });
    });    
    
    // Updates downvotes for posts
    $('.post-downvotes').each(function () {
        $(this).click(function(){            
            var postid;
            postid = $(this).attr("data-post-id");  
            $.get('/preggo/downvote_post/', {post_id: postid},                                           function(data, status){
                var selector = "#post-downvotes-count-" + postid;                                
                $(selector).html(data);
            });
                            
        });
    });    
    
    // Get search results
    $("#search_form").submit(function(event) {
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        
        $.get(url, {},
            function(data) {
                $("#search-results").html(data);
            });
    });
    
    
    
    $(".comment-box").hide();
    
    $(".comment-link").click(function(event) {
        event.preventDefault();
        var id = $(this).attr("data-textarea-id");        
        if (!$("#"+id).is(":visible")) {
            $("#"+id).show();
        }
    });
    
    $(".comment-box").keypress(function(evt) {
        evt.preventDefault();
        if (evt.which == 13) {
            console.log("submit the comment");
        }
    });
    
//     $(".clickable").click(function(evt) {        
//         var obj_id = $(this).attr("data-post-id");
//         console.log("clicked");
//     });
    
    var showCommentBox = function () {
//         $("#comment-box").show();
    }
});


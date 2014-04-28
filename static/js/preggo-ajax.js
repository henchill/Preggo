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
});
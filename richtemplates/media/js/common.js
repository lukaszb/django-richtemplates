/*
   Some common javascripts which may be useful.
   Scripts require jQuery to run.
*/

$(document).ready(function()
{
    $('.richtemplates-popup').each(function(){
        var height = $(this).height();
        var width = $(this).width();
        
        leftVal=e.pageX-(width/2)+"px";
        topVal=e.pageY-(height/2)+"px";
        
        $('#popuup_div').css({left:leftVal,top:topVal}).show().fadeOut(2500);
    });
});

function textarea_stabilizator(ta){
    // Dynamically changes textareas' height
    var content = ta.val();
    var content_length = content.split('\n').length;
    var rows = ta.attr('rows');

    console.log("Textarea content length is: " + content_length);

    if (content_length <10){
        ta.attr('rows', '10');
    }
    else if (content_length >= rows) {
        ta.attr('rows', content_length);
    }
    else if (content_length < rows+1) {
        ta.attr('rows', rows-1);
    }
}

$(document).ready(function(){
    $('textarea').each(function(){
        textarea_stabilizator($(this));
    });
    $('textarea').keyup(function(){
        textarea_stabilizator($(this));
    });
});


// from http://www.djangosnippets.org/snippets/1488/
jQuery.fn.slugify = function(obj) {
    jQuery(this).data('obj', jQuery(obj));
    jQuery(this).keyup(function() {
        var obj = jQuery(this).data('obj');
        var slug = jQuery(this).val().replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
        obj.val(slug);
    });
}




/*
   Some common javascripts which may be useful.
   Scripts require jQuery to run.
*/

function textarea_stabilizator(ta){
    // Dynamically changes textareas' height
    var content = ta.val();
    var content_length = content.split('\n').length;
    var rows = ta.attr('rows');

    if (content_length <10){
        ta.attr('rows', '10');
    }
    else if (content_length >= rows) {
        ta.attr('rows', content_length);
    }
    else if (content_length < rows+1) {
        ta.attr('rows', rows-1);
    }

    ta.attr('cols', 80);
}

$(document).ready(function(){
    $('textarea').each(function(){
        textarea_stabilizator($(this));
    });
    $('textarea').click(function(){
        textarea_stabilizator($(this));
    });
    $('textarea').keyup(function(){
        textarea_stabilizator($(this));
    });

    /* Tipsy tooltips */
    $('.show-tipsy').tipsy({
        gravity: 's'
    });
    $('.show-tipsy-bottom').tipsy({
        gravity: 'n'
    });
    $('.show-tipsy-left').tipsy({
        gravity: 'e'
    });
    $('.show-tipsy-right').tipsy({
        gravity: 'w'
    });

    /* Datepicker */
    $('input.datepicker').datepicker({
        dateFormat: 'yy-mm-dd',
        firstDay: 1,
        showButtonPanel: true,
        showAnim: 'show',
        showOn: 'button',
        buttonImage: '/media/richtemplates/img/ruby-calendar.gif',
        buttonImageOnly: true
    });

    $('a.togglable').each(function(){
        $(this).togglable({
            showLabel: $(this).text()
        });
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




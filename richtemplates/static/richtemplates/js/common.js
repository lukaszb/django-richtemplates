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

    /* ************************ *
     * jQuery UI common scripts *
     * ************************ */

    $('input.datepicker').datepicker({
        dateFormat: 'yy-mm-dd', //TODO: Use L10N
        firstDay: 1,
        showButtonPanel: true,
        showAnim: 'show',
        showOn: 'button',
        buttonImage: '/media/richtemplates/img/calendar.png', //TODO: Dont hardcode url
        buttonImageOnly: true
    });

    $('a.togglable').each(function(){
        $(this).togglable({
            showLabel: $(this).text()
        });
    });

    $('.richtabs').tabs();
    $('.richbutton .button-link').removeClass('button-link');
    $('.richbutton').button();
    $('.richbutton-wrench.button-link').removeClass('button-link');
    $('.richbutton-wrench').button({icons: { primary: "ui-icon-wrench" }});
    $('.richbuttonset .button-link').removeClass('button-link');
    $('.richbuttonset').buttonset();

    $('#global-messages li').hover(
        function(){
            $(this).stop().addClass('border-gray').addClass('to-be-closed');
        },
        function(){
            if (!$(this).hidden){
                $(this).stop().removeClass('border-gray').removeClass('to-be-closed');
            }
        }
    );
    $('#global-messages li').click(function(){
        $(this).hide();
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
};


// jQuery jqplot extras
// extra function for bar plots until jqplot fully support bar charts' tooltips

function make_richplot(plot){
        console.log(plot);

        $('div.jqplot-point-label', plot).each(function(){
            var elem = $(this);
            var text = elem.text();
            elem.attr('title', text);
            var width = elem.width();
            elem.text('');
            elem.width(width);
            elem.tipsy({gravity: 's', trigger: 'manual'});
        });

        plot.bind('jqplotDataHighlight', 
            function (ev, seriesIndex, pointIndex, data) {
                var pointLabel = $('div.jqplot-point-label.jqplot-series-' + seriesIndex + '.jqplot-point-' + pointIndex, plot);
                pointLabel.tipsy("show");
                pointLabel.hide();

            }
        );

        plot.bind('jqplotDataUnhighlight', 
            function (ev, seriesIndex, pointIndex, data) {
                var pointLabel = $('div.jqplot-point-label', plot);
                $('div.jqplot-point-label', plot).each(function(){
                    $(this).tipsy("hide");
                    $(this).show();
                });
            }
        );
}

// Django 1.3 Ajax & CSRF

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


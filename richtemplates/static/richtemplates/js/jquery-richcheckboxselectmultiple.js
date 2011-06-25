$(document).ready(function(){
    var selector = '.richcheckboxselectmultiple';
    var tbody = $('tbody', selector);
    var tfoot = $('tfoot', selector);

    $('tr', tbody)
        .filter(':has(:checkbox:checked)')
        .addClass('ui-selected')
        .end()
    .click(function(event){
        var checkbox = $(':checkbox', this);
        if (event.target.nodeName != 'LABEL'){
            //$(this).toggleClass('ui-selected');
            if (event.target.type != 'checkbox'){
                checkbox.attr('checked', function(){
                    return !this.checked;
                });
            }
        }
        if (checkbox.attr('checked')){
            $(this).addClass('ui-selected');
        } else {
            $(this).removeClass('ui-selected');
        }
    });

    $('.select-all', tfoot).click(function(){
        $('tr:not(.ui-selected)', tbody).click();
    });
    $('.deselect-all', tfoot).click(function(){
        $('tr.ui-selected', tbody).click();
    });
    $('.change-all', tfoot).click(function(){
        $('tr', tbody).click();
    });
});


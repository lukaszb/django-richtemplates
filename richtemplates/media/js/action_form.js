$(document).ready(function(){
    // Simple function enabling/disabling object(s)
    $.fn.enable = function(enabled) {
        return this.each(function() {
            this.disabled = !enabled;
    });
  }

    function processActionForm(selectedAction){
        $('form.action-form input:radio[name=action_type]').each(function(){
            if ( selectedAction != $(this) ){
                var wrapper = $(this).parent();
                $(':input:not(:radio)', wrapper).each(function(){
                    $(this).addClass('disabled').enable(false);
                });
                wrapper.addClass('disabled');
            }
        });
        // Enable selected field
        var wrapper = selectedAction.parent();
        $(':input:not(:radio)', wrapper).each(function(){
            $(this).removeClass('disabled').enable(true);
        });
        wrapper.removeClass('disabled');
        $(':input:not(:radio):first', wrapper).focus();
    }
    
    $('form.action-form input:radio').change(function(){
        processActionForm($(this));
    });

    $('form.action-form input:radio:checked').each(function(){
        processActionForm($(this));
    });

});

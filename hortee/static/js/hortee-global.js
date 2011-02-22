var hortee = {
    messages: {
        hide_timeout: 5000,
        add: function(msg, tag) {
            var tag = tag || 'info';            
            idx = $('ul.messages').append($('<li class="'+ tag +'">'+ msg +'</li>')).find('li').length-1;
            hortee.messages.hide(idx);
        },
        hide: function(idx) {
            window.setTimeout(function(){ 
                $($('ul.messages li').get(idx)).hide();
            }, hortee.messages.hide_timeout);
        },
        debug: function(msg)   { return hortee.messages.add(msg, 'debug'); },
        info: function(msg)    { return hortee.messages.add(msg, 'info'); },
        success: function(msg) { return hortee.messages.add(msg, 'success'); },
        warning: function(msg) { return hortee.messages.add(msg, 'warning'); },
        error: function(msg)   { return hortee.messages.add(msg, 'error'); }
    }
};


$(function() {
    // Mustache style templates for underscore
    _.templateSettings = {
        evaluate    : /{%([\s\S]+?)%}/g,
        interpolate : /{{([\s\S]+?)}}/g
    };
});


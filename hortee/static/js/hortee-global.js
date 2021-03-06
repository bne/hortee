function Messages() {
    var add = function(msg, tag) {
        var tag = tag || 'info';            
        idx = $('ul.messages').append(
            $('<li class="'+ tag +'">'+ msg +'</li>')).find('li').length-1;
        hide(idx);
    };
    var hide = function(idx) {
        _.delay(function(){
            $('ul.messages li').get(idx).style.display = 'none'; 
        }, 5000);
    };        
    var rtn = { add: add, hide: hide };  
    _(['debug', 'info', 'success', 'warning', 'error']).each(function(tag) {
        rtn[tag] = function(msg) { this.add(msg, tag); };
    });    
    return rtn;
}

formatDate = function(d) {
    function Z(n) { return ('0'+n).substr(-2); }
    d = new Date(d);
    return d.getFullYear() +'-'+ Z(d.getMonth()) +'-'+ Z(d.getDate()) 
        +' '+ Z(d.getHours()) +':'+ Z(d.getMinutes()); 
}

$(function() {
    // Mustache style templates for underscore
    _.templateSettings = {
        evaluate    : /{%([\s\S]+?)%}/g,
        interpolate : /{{([\s\S]+?)}}/g
    };
    
    window.messages = new Messages();
});



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

Date.prototype.formatDate = function() {
    function Z(n) { return ((n+'').length==1?'0':'') + n; }
    return this.getFullYear() + '-' + Z(this.getMonth()) + '-' + 
        Z(this.getDate()) + ' ' + Z(this.getHours()) + ':' + Z(this.getMinutes()); 
}

$(function() {
    // Mustache style templates for underscore
    _.templateSettings = {
        evaluate    : /{%([\s\S]+?)%}/g,
        interpolate : /{{([\s\S]+?)}}/g
    };
    
    window.messages = new Messages();
});


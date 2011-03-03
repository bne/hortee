$(function(){
    // Reimplements Backbone.sync to add the django xsrf token as a cookie
    // Requires the rejiggled zepto.js that allows headers in the ajax options

    function trim(str) {
        str = str.replace(/^\s+/, '');
        for(var i=str.length-1; i>0; -i) {
            if( /\S/.test( str[i] ) ) {
                str = str.substring(0, i+1);
                break;
            }
        }
        return str;
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    var methodMap = {
        'create': 'POST',
        'update': 'PUT',
        'delete': 'DELETE',
        'read'  : 'GET'
    };
    
    // Helper function to get a URL from a Model or Collection as a property
    // or as a function.
    var getUrl = function(object) {
        if (!(object && object.url)) throw new Error("A 'url' property or function must be specified");
        return _.isFunction(object.url) ? object.url() : object.url;
    };    

    Backbone.sync = function(method, model, success, error) {
        var type = methodMap[method];
        var modelJSON = (method === 'create' || method === 'update') ?
                        JSON.stringify(model.toJSON()) : null;

        // Default JSON-request options.
        var params = {
            url:          getUrl(model),
            type:         type,
            contentType:  'application/json',
            data:         modelJSON,
            dataType:     'json',
            processData:  false,
            success:      success,
            error:        error
        };

        // get round django's new fangled xsrf protection
        if (!(/^http:.*/.test(params.url) || /^https:.*/.test(params.url))) {
            // Only send the token to relative URLs i.e. locally.
            params['headers'] = ['X-CSRFToken', getCookie('csrftoken')];
        }
        
        // For older servers, emulate JSON by encoding the request into an HTML-form.
        if (Backbone.emulateJSON) {
            params.contentType = 'application/x-www-form-urlencoded';
            params.processData = true;
            params.data        = modelJSON ? {model : modelJSON} : {};
        }

        // For older servers, emulate HTTP by mimicking the HTTP method with `_method`
        // And an `X-HTTP-Method-Override` header.
        if (Backbone.emulateHTTP) {
            if (type === 'PUT' || type === 'DELETE') {
                if (Backbone.emulateJSON) params.data._method = type;
                params.type = 'POST';
                params.beforeSend = function(xhr) {
                    xhr.setRequestHeader("X-HTTP-Method-Override", type);
                };
            }
        }
        
        //console.log(params);

        // Make the request.
        $.ajax(params);
    };
});

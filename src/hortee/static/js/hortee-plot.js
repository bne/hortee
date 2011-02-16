$(function(){
    function set_lat_lng() {
        navigator.geolocation.getCurrentPosition(
            function(pos) {
                $('#id_lat').val(pos.coords.latitude);
                $('#id_lng').val(pos.coords.longitude);
            }, 
            function(msg) {
                console.log(msg);
            }
        );    
    }
    
    if(navigator.geolocation) {
        if(!$('#id_lat').val() && !$('#id_lng').val()) {
            set_lat_lng();
        }        
        $('#coords').append($('<a>', { 
            text: 'Update coords',
            click: set_lat_lng
        }));
    }
});


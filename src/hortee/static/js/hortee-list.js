$(function(){
    $('#actors li').click(function(){
        var events = $(this).find('ul.events');
        if(!events.html()) {
            $.get('/list/'+this.id, function(data){
                events.append(data);
                events.slideDown();
            });
        }
        else {
            events.slideToggle();
        }
    });
});

$(function(){
    $('#add_actor input[type="button"]').click(function(){
        $.post('/actor/add/', { name: $('#actor_name').val() }, function(data){
            $('#actors').prepend(data);
        });
    });

    $('#actors li').click(function(){
        var events = $(this).find('ul.events');
        if(!events.html()) {
            $.get('/list/'+this.id.replace(/[^\d]+/,'')+'/', function(data){
                events.append(data);
                events.slideDown();
            });
        }
        else {
            events.slideToggle();
        }
    });
    
    $('#actors li span.delete').click(function(){
        
    });
});

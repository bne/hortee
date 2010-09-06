$(function(){
    $('#add_actor').submit(function(){
        $.post('/actor/add/', 
          { name: $(this).find('input[type="text"]').val() }, function(data){
            $('#actors').prepend(data);
        });
        return false;
    });
    
    $('form.add_event').submit(function(){
        var events = $(this).parent().find('ul.events');
        $.post('/event/add/', { 
          name: $(this).find('input[type="text"]').val(),
          actor_id: $(this).find('input[type="hidden"]').val()
        }, function(data){
            events.prepend(data);
        });
        return false;
    });

    $('#actors li span.name').click(function(){
        var parent = $(this).parent().get(0);
        var events = $(parent).find('ul.events');
        if(!events.html()) {
            $.get('/list/'+parent.id.replace(/[^\d]+/,'')+'/', function(data){
                events.append(data);
                events.slideDown();
            });
        }
        else {
            events.slideToggle();
        }
    });
    
    $('li').delegate('span.delete', 'click', function(ev){
        var parent = $(this).parent().get(0);
        var id = parent.id.split('_');
        $.post('/'+ id[0] +'/delete/', { id: id[1] }, function(data){
            if(data) {
                $(parent).remove();
            }
        });
    });
});

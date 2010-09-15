$(function(){
    $('#add_actor').submit(function(){
        var name_fld = $(this).find('input[type="text"]');
        $.post('/actor/add/', 
          { 'name': name_fld.val() }, function(data){
            name_fld.val('');
            $('#actors').prepend(data);
        });
        return false;
    });
    
    $('#actors li span.name').live('click', function(){
        var actor_id = $(this).parent().get(0).id;
        var ul = $(this).parent().find('ul.events');
        var fm = $(this).parent().find('form.add_event');
        if(!ul.html()) {
            $.get('/list/'+actor_id.replace(/[^\d]+/,'')+'/', function(data){
                ul.append(data);
                ul.slideDown();
                fm.slideDown();
            });
        }
        else {
            ul.slideToggle();
            fm.slideToggle();
        }        
    });
        
    $('form.add_event').live('submit', function(){
        var actor_id = $(this).find('input[type="hidden"]').val();
        var name_fld = $(this).find('input[type="text"]');
        $.post('/event/add/', { 
          'name': name_fld.val(),
          'actor_id': actor_id
        }, function(new_event){
            name_fld.val('');
            $('#actor_'+ actor_id + ' ul.events').append(new_event);
        });
        return false;
    });
    
    $('li').delegate('span.delete', 'click', function(ev){
        if(!confirm('Are you sure you want to delete?')) {
            return false;
        }
        var parent = $(this).parent().get(0);
        var id = parent.id.split('_');
        $.post('/'+ id[0] +'/delete/', { id: id[1] }, function(data){
            if(data) {
                $(parent).remove();
            }
        });
    });
});

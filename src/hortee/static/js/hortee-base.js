$(function(){
    $('#add_plot').hide();
    
    $('#lnk_add_plot').click(function(){
        $('#add_plot').show();
        return false;
    });
    
    $('#add_plot').submit(function(){
        var name_fld = $(this).find('input[type="text"]');
        $.post('/plot/add/', 
          { 'name': name_fld.val() }, function(data){
            name_fld.val('');
            $('#plots').html(data);
        });
        return false;
    });    
});

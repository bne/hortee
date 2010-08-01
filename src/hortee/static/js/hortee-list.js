$(function(){
    $('#actors li').click(function(){
        $.get('/list/'+this.id, function(data){
            
        });
    });
});

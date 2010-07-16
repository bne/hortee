$(function(){
    var canvas = $('canvas');
    var ctx = canvas.get(0).getContext('2d');  

    var bg_col = '#FFFF00';
    var fg_col = '#00FF00';
    var ac_col = '#FF0000';     
    var drag_start = false;
    var start_pos = { x:0, y:0 };    
    var end_pos = { x:0, y:0 };

    canvas.attr('height', $(document).height());
    canvas.attr('width', $(document).width());
    
    $(document).mousedown(function(ev){
        ctx.save();
        drag_start = true;
        start_pos.x = end_pos.x = ev.pageX;
        start_pos.y = end_pos.y = ev.pageY;
    });
    
    $(document).mousemove(function(ev){
        if(drag_start){
            ctx.clearRect(0, 0, canvas.width(), canvas.height());
            ctx.strokeStyle = ac_col;
            ctx.strokeRect(
                start_pos.x, start_pos.y, 
                ev.pageX - start_pos.x, ev.pageY - start_pos.y);
            ctx.restore();
        }
    });
    
    $(document).mouseup(function(ev){
        if(drag_start){
            ctx.strokeStyle = fg_col;
            ctx.strokeRect(
                start_pos.x, start_pos.y, 
                ev.pageX - start_pos.x, ev.pageY - start_pos.y);

            drag_start = false;
        }
    }); 
});

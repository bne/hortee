$(function(){
    var canvas = $('canvas');
    var ctx = canvas.get(0).getContext('2d');  

    var bg_col = '#FFFF00';
    var fg_col = '#00FF00';
    var ac_col = '#FF0000';    
     
    var drag_start = false;
    var start_pos;
    var sprites = [];
    
    canvas.attr('height', $(document).height());
    canvas.attr('width', $(document).width());
    
    $(document).mousedown(function(ev){
        drag_start = true;
        start_pos = { 'x': ev.pageX, 'y': ev.pageY };
    });
    
    $(document).mousemove(function(ev){
        if(drag_start){
            ctx.clearRect(0, 0, canvas.width(), canvas.height());
            ctx.beginPath();
            ctx.rect(start_pos.x, start_pos.y, 
                ev.pageX - start_pos.x, ev.pageY - start_pos.y);
            ctx.strokeStyle = ac_col;
            ctx.stroke();
            draw();
        }
        
        //console.log(ctx.isPointInPath(ev.pageX, ev.pageY));        
    });
    
    $(document).mouseup(function(ev){
        if(drag_start){
            
            sprites.push({
                'path': [
                    {'shape': 'rect', 'args': [start_pos.x, start_pos.y, ev.pageX - start_pos.x, ev.pageY - start_pos.y]}
                ]
            });
            
            drag_start = false;
            draw();
        }
    });
    
    function draw() {        
        for(var i=0, sprite; sprite=sprites[i]; i++) {
            ctx.beginPath();
            ctx.strokeStyle = fg_col;
            for(var j=0, shape; shape=sprite.path[j]; j++) {
                ctx[shape.shape].apply(ctx, shape.args);
            }
            ctx.stroke();
            ctx.closePath();
        }        
    }
});

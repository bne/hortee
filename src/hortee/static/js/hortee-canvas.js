$(function(){
    var canvas = $('canvas').get(0);
    var p = Processing(canvas);
    p.size($(document).width(), $(document).height());
    p.stroke(255);
    
    function draw(p) {
        p.rect(
            start_pos.x, start_pos.y, 
            end_pos.x - start_pos.x, end_pos.y - start_pos.y);
    }
        
    var drag_start = false;
    var start_pos = { x:0, y:0 };
    var end_pos = { x:0, y:0 };
    
    $(document).mousedown(function(ev){
        drag_start = true;
        start_pos.x = ev.pageX;
        start_pos.y = ev.pageY;
    });
    
    $(document).mousemove(function(ev){
        end_pos.x = ev.pageX;
        end_pos.y = ev.pageY;
    });
    
    $(document).mouseup(function(ev){
        drag_start = false;
        draw(p);
    });
});

$(function(){
    var canvas = $('canvas').get(0);
    var p = Processing(canvas);
    p.size($(document).width(), $(document).height());
    p.stroke(0);
    
    var cur_sh = 'rect';
    var sh = [];

        
    var drag_start = false;
    var start_pos = { x:0, y:0 };
    var end_pos = { x:0, y:0 };
    
    $(document).mousedown(function(ev){
        drag_start = true;
        start_pos.x = ev.pageX;
        start_pos.y = ev.pageY;
    });
    
    $(document).mousemove(function(ev){
        if(drag_start){
            end_pos.x = ev.pageX;
            end_pos.y = ev.pageY;
            p[cur_sh].apply(this, [start_pos.x, start_pos.y, 
                end_pos.x - start_pos.x, end_pos.y - start_pos.y]);            
            draw(p);
        }
    });
    
    $(document).mouseup(function(ev){
        drag_start = false;
        sh.push([cur_sh, [start_pos.x, start_pos.y, 
            end_pos.x - start_pos.x, end_pos.y - start_pos.y]]);
    });    
    
    function draw(p) {
        for(var i=0;i<sh.length;i++){
            p.noFill();
            p[sh[i][0]].apply(this, sh[i][1]);
        }
    }
});

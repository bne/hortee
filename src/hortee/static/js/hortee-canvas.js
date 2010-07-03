$(function(){
    var canvas = $('canvas');
    var p = Processing(canvas.get(0));
    var cur_sh = 'rect';
    var sh = [];     
    var bg_col = '#FFFFFF';
    var fg_col = '#000000';
    var ac_col = '#FF0000';     
    var drag_start = false;
    var start_pos = { x:0, y:0 };
    var end_pos = { x:0, y:0 };

    function resize_canvas(){    
        canvas.attr('height', $(document).height());
        canvas.attr('width', $('#header').width());
        p = Processing(canvas.get(0));
        draw();
    }
    $(window).resize(resize_canvas);
    resize_canvas();
    
    $(document).mousedown(function(ev){
        drag_start = true;
        start_pos.x = end_pos.x = ev.pageX;
        start_pos.y = end_pos.y = ev.pageY;
    });
    
    $(document).mousemove(function(ev){
        if(drag_start){        
            p.background(bg_col);
            p.stroke(ac_col);
            end_pos.x = ev.pageX;
            end_pos.y = ev.pageY;
            p[cur_sh].apply(this, [start_pos.x, start_pos.y, 
                end_pos.x - start_pos.x, end_pos.y - start_pos.y]);
            draw();           
        }
    });
    
    $(document).mouseup(function(ev){
        if(drag_start){
            sh.push([cur_sh, [start_pos.x, start_pos.y, 
                end_pos.x - start_pos.x, end_pos.y - start_pos.y]]);
            draw();
            drag_start = false;
        }
    });    
    
    function draw() {
        p.stroke(fg_col);
        for(var i=0;i<sh.length;i++){
            p.noFill();
            p[sh[i][0]].apply(this, sh[i][1]);
        }
    }
});

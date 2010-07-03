$(function(){
    var canvas = $('canvas');
    var p = Processing(canvas.get(0));
    var cur_shape = 'rect';
    var sprites = [];     
    var bg_col = '#FFFFFF';
    var fg_col = '#000000';
    var ac_col = '#FF0000';     
    var drag_start = false;
    var start_pos = { x:0, y:0 };
    var end_pos = { x:0, y:0 };

    function resize_canvas(){    
        canvas.attr('height', $(document).height());
        canvas.attr('width', $(document).width());
        p = Processing(canvas.get(0));
        draw();
    }
    $(window).resize(resize_canvas);
    resize_canvas();
    
    function serialise(){
        return sprites.join(',');
    }
    
    $(document).mousedown(function(ev){
        drag_start = true;
        start_pos.x = end_pos.x = ev.pageX;
        start_pos.y = end_pos.y = ev.pageY;
    });
    
    $(document).mousemove(function(ev){
        if(drag_start){        
            p.background(bg_col);
            p.stroke(ac_col);
            p.noFill();
            end_pos.x = ev.pageX;
            end_pos.y = ev.pageY;
            p[cur_shape].apply(this, [start_pos.x, start_pos.y, 
              end_pos.x - start_pos.x, end_pos.y - start_pos.y]);
            draw();           
        }
    });
    
    $(document).mouseup(function(ev){
        if(drag_start){
            sprite = [cur_shape, [start_pos.x, start_pos.y, 
              end_pos.x - start_pos.x, end_pos.y - start_pos.y]];
                        
            if(!sprites.length || 
              (sprites.length && 
              (sprite.join() != sprites[sprites.length-1].join()))){
                sprites.push(sprite);
            }
            draw();
            drag_start = false;
        }
        console.log(serialise());
    });    
    
    function draw() {
        p.stroke(fg_col);
        for(var i=0;i<sprites.length;i++){
            p.noFill();
            p[sprites[i][0]].apply(this, sprites[i][1]);
        }
    }
});

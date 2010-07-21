$(function(){

    var canvas = $('canvas');
<<<<<<< HEAD
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
=======
    var map = $('map');    
    var mapimg = $('#mapimg');    
    var ctx = canvas.get(0).getContext('2d');
    var cur_path = { 
        'shape': 'rect', 'stroke': '#698B22', 'fill': '#FAFAD2',
        'lineWidth': 4, 'lineJoin': 'round',    
    };     
    var guide_path = { 
        'shape': cur_path.shape, 'stroke': '#999', 
        'fill': 'transparent', 'lineWidth': 1
    };
    var drag_start = false;
    var start_pos;
    var sprites = [];
    var cur_sprite_id;
    var old_sprite;
    var old_offset;
    
    canvas.attr('height', $(document).height());
    canvas.attr('width', $(document).width());
    
    mapimg.attr('height', $(document).height());
    mapimg.attr('width', $(document).width());
    
    $(document).mousedown(function(ev) {
>>>>>>> c6523517c4e611278547d985b2d98403188dd589
        drag_start = true;
        start_pos = { 'x': ev.pageX, 'y': ev.pageY };
        
        canvas.css('z-index', 1000);
        mapimg.css('z-index', 1);
        
        if(cur_sprite_id) {
            old_offset = { 
                'x': ev.pageX - old_sprite.paths[0].args[0],
                'y': ev.pageY - old_sprite.paths[0].args[1]
            };
        }
    });
<<<<<<< HEAD
    
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
=======

    $(document).mousemove(function(ev) {
        if(drag_start) {
            if(!cur_sprite_id) {
                guide_path.args = [
                    start_pos.x + (guide_path.lineWidth / 2), 
                    start_pos.y + (guide_path.lineWidth / 2), 
                    ev.pageX - start_pos.x, 
                    ev.pageY - start_pos.y
                ];
                draw_sprites();
                draw_path(guide_path);
            }
            else {
                sprites[cur_sprite_id].paths[0].args[0] = ev.pageX - old_offset.x;
                sprites[cur_sprite_id].paths[0].args[1] = ev.pageY - old_offset.y;                
                draw_sprites();
            }
        }
    });
    
    $(document).mouseup(function(ev) {
        canvas.css('z-index', 1);
        mapimg.css('z-index', 1000);
                
        if(drag_start && !cur_sprite_id && 
          Math.abs(start_pos.x - ev.pageX) > 10 && 
          Math.abs(start_pos.y - ev.pageY) > 10) {
           
            cur_path.args = [
                start_pos.x + (cur_path.lineWidth / 2), 
                start_pos.y + (cur_path.lineWidth / 2), 
                ev.pageX - start_pos.x, 
                ev.pageY - start_pos.y
            ];
            sprites.push({'paths': [$.extend({}, cur_path)]});
            
            map.prepend('<area shape="rect" coords="'+ [
                start_pos.x,
                start_pos.y,
                ev.pageX,
                ev.pageY
            ].join(',') +'" id="area_'+ (sprites.length - 1) +'" />');
        }
        
        if(drag_start && cur_sprite_id) {
            console.log('foo');
            $('#area_'+ cur_sprite_id).attr('coords', [
                sprites[cur_sprite_id].paths[0].args[0],
                sprites[cur_sprite_id].paths[0].args[1],
                sprites[cur_sprite_id].paths[0].args[0] + sprites[cur_sprite_id].paths[0].args[2],
                sprites[cur_sprite_id].paths[0].args[1] + sprites[cur_sprite_id].paths[0].args[3]
            ].join(','));
>>>>>>> c6523517c4e611278547d985b2d98403188dd589
        }
        
        draw_sprites();
        drag_start = false;
    });
    
    map.delegate('area', 'mouseover', function() {
        cur_sprite_id = this.id.substr(this.id.indexOf('_')+1);
        old_sprite = $.extend({}, sprites[cur_sprite_id]);
        sprites[cur_sprite_id].paths[0].fill = '#F00';
        draw_sprites();
    });
    
    map.delegate('area', 'mouseout', function() {
        if(!drag_start) {            
            sprites[cur_sprite_id].paths[0].fill = cur_path.fill;
            draw_sprites();                        
            cur_sprite_id = old_sprite = null;
        }            
    });
    
    function draw_sprites() {
        ctx.clearRect(0, 0, canvas.width(), canvas.height());
        $.each(sprites, function(i, sprite) {
            $.each(sprite.paths, function(i, path) { 
                draw_path(path); 
            })
        });
    }
    
    function draw_path(_path) {
        ctx.lineWidth = _path.lineWidth;
        ctx.lineJoin = _path.lineJoin;
        ctx.strokeStyle = _path.stroke;
        ctx.fillStyle = _path.fill;
          
        ctx.beginPath();
        ctx[_path.shape].apply(ctx, _path.args);
        ctx.fill();
        ctx.stroke();
    }
});

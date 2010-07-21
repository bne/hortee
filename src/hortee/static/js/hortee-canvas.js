$(function(){

    var canvas = $('canvas');
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
    var sprite_id;
    
    canvas.attr('height', $(document).height());
    canvas.attr('width', $(document).width());
    
    mapimg.attr('height', $(document).height());
    mapimg.attr('width', $(document).width());
    
    $(document).mousedown(function(ev) {
        drag_start = true;
        start_pos = { 'x': ev.pageX, 'y': ev.pageY };
        
        canvas.css('z-index', 1000);
        mapimg.css('z-index', 1);
    });

    $(document).mousemove(function(ev) {
        if(drag_start) {
            guide_path.args = [
                start_pos.x + (guide_path.lineWidth / 2), 
                start_pos.y + (guide_path.lineWidth / 2), 
                ev.pageX - start_pos.x, 
                ev.pageY - start_pos.y
            ];
            draw_sprites();
            draw_path(guide_path);
        }
    });
    
    $(document).mouseup(function(ev) {
        canvas.css('z-index', 1);
        mapimg.css('z-index', 1000);
        
        if(drag_start && 
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
        draw_sprites();
        drag_start = false;     
    });
    
    map.delegate('area', 'mouseover', function() {
        sprite_id = this.id.substr(this.id.indexOf('_')+1);
        sprites[sprite_id].paths[0].fill = '#F00';
        draw_sprites();
    });
    
    map.delegate('area', 'mouseout', function() {
        sprites[sprite_id].paths[0].fill = cur_path.fill;
        sprite_id = null;
        draw_sprites();
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

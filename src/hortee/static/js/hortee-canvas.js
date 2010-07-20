$(function(){
    var canvas = $('canvas');
    var map = $('map');
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
    
    canvas.attr('height', $(document).height());
    canvas.attr('width', $(document).width());
    map.attr('height', $(document).height());
    map.attr('width', $(document).width());
    
    $(document).mousedown(function(ev) {
        drag_start = true;
        start_pos = { 'x': ev.pageX, 'y': ev.pageY };
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
        if(drag_start) {            
            cur_path.args = [
                start_pos.x + (cur_path.lineWidth / 2), 
                start_pos.y + (cur_path.lineWidth / 2), 
                ev.pageX - start_pos.x, 
                ev.pageY - start_pos.y
            ];
            sprites.push({'paths': [$.extend({}, cur_path)]});            
            drag_start = false;
            draw_sprites();
            
            map.append('<area shape="rect" coords="'+ cur_path.args.join(',') +'" onmouseover="alert(2);" />');
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

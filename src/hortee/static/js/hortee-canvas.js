$(function(){
    var canvas = $('canvas').get(0);
    var p = Processing(canvas);
    p.size($(document).width(), $(document).height());
    p.stroke(255);
    
    function draw(p) {
        p.background(0);
        y = y - 1;
        if (y < 0) y = p.height;
        p.line(0, y, p.width, y);
    }
    var y = 100;
    var frameRate = 90;
    var interval = 1000.0 / frameRate;
    
    draw(p);
    //setInterval(function () { draw(p); }, interval);
});

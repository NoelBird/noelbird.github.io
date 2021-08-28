var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var x = canvas.width/2;
var y = canvas.height-30;
var dx = 2;
var dy = -2;
var ballRadius = 10;
var color = "rgb(3,3,3,1)";

function drawBall(){
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI*2);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}
function draw(){
    // drawing code
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBall();
    if(x + dx > canvas.width - ballRadius || x + dx < ballRadius){
        dx = -dx;
        color = "#" + Math.floor(Math.random()*255*255*255).toString(16);
    }
    if(y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
        dy = -dy;
        color = "#" + Math.floor(Math.random()*255*255*255).toString(16);
        console.log(color);
    }
    x += dx;
    y += dy;
    
    
}

setInterval(draw, 10); // per 10 milli seconds
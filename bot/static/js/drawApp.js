var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

var drawingAreaX = 0;
var drawingAreaY = 0;
var drawingAreaWidth = tx; //image width
var drawingAreaHeight = ty; //image height

var colorRed = "#ff0000";
var colorGreen = "#00ff00";
var colorBlue = "#0000ff";

var curColor = colorRed;
var clickColor = new Array();

context = document.getElementById('canvas').getContext("2d");
outlineImage.onload = function(){ // load at the beginning
  // image  has been loaded
  context.drawImage(outlineImage, drawingAreaX, drawingAreaY, drawingAreaWidth, drawingAreaHeight);
};

$('#canvas').mousedown(function(e){
  var sidewidth = document.getElementById("navbar").offsetWidth; //sidebar width
  var topheight = document.getElementById("topbar").offsetHeight; //top navbar width
  var mouseX = e.pageX - this.offsetLeft - sidewidth;
  var mouseY = e.pageY - this.offsetTop - topheight;
  paint = true;
  addClick(mouseX, mouseY);
  redraw();
});

$('#canvas').mousemove(function(e){
  if(paint){
    var sidewidth = document.getElementById("navbar").offsetWidth; //sidebar width
    var topheight = document.getElementById("topbar").offsetHeight; //top navbar width
    addClick(e.pageX - this.offsetLeft - sidewidth, e.pageY - this.offsetTop - topheight, true);
    redraw();
  }
});

$('#canvas').mouseup(function(e){
  paint = false;
});

$('#canvas').mouseleave(function(e){
  paint = false;
});

function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
  clickColor.push(curColor);
}

function redraw(){
  context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
  // Draw the outline image
  context.drawImage(outlineImage, drawingAreaX, drawingAreaY, drawingAreaWidth, drawingAreaHeight);

  context.lineJoin = "round";
  context.lineWidth = 5;

  for(var i=0; i < clickX.length; i++) {
    context.beginPath();
    if(clickDrag[i] && i){
      context.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       context.moveTo(clickX[i]-1, clickY[i]);
     }
     context.lineTo(clickX[i], clickY[i]);
     context.closePath();
     context.strokeStyle = clickColor[i];
     context.stroke();
  }
}

//clear function
$('#clearCanvas').mousedown(function(e)
	{
    clickX = new Array();
		clickY = new Array();
		clickDrag = new Array();
    clickColor = new Array();
		context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    // load image after cleaning
    context.drawImage(outlineImage, drawingAreaX, drawingAreaY, drawingAreaWidth, drawingAreaHeight);
	});

// color
$('#chooseRed').mousedown(function(e){
		curColor = colorRed;
	});
$('#chooseGreen').mousedown(function(e){
		curColor = colorGreen;
	});
$('#chooseBlue').mousedown(function(e){
		curColor = colorBlue;
	});


//redraw without background image before save
function redraw2(){
  context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
  context.lineJoin = "round";
  context.lineWidth = 5;

  for(var i=0; i < clickX.length; i++) {
    context.beginPath();
    if(clickDrag[i] && i){
      context.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       context.moveTo(clickX[i]-1, clickY[i]);
     }
     context.lineTo(clickX[i], clickY[i]);
     context.closePath();
     context.strokeStyle = clickColor[i];
     context.stroke();
  }
}

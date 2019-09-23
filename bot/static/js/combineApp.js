var fgImage = null;
var bgImage = null;
var fgcan = null;
var bgcan = null;

function loadForegroundImage() {
  var imgFile = document.getElementById("fgfile");
  fgImage = new SimpleImage(imgFile);
  fgcan = document.getElementById("fgcan");
  fgImage.drawTo(fgcan);
  //alert("foreground image loaded!");
}

function loadBackgroundImage() {
  var imgFile = document.getElementById("bgfile");
  bgImage = new SimpleImage(imgFile);
  bgcan = document.getElementById("bgcan");
  bgImage.drawTo(bgcan);
  //alert("background image loaded!");
}

function doGreenScreen() {
  if (fgImage == null || ! fgImage.complete()) {
  alert("沒有前景圖");
  return;
  }
  if (bgImage == null || ! bgImage.complete()) {
  alert("沒有背景圖");
  }
  clearCanvas();

  var output = new SimpleImage(fgImage.getWidth(), fgImage.getHeight());

  for(var pixel of fgImage.values()) {
    var x = pixel.getX();
    var y = pixel.getY();
    //filter here
    if (pixel.getBlue() + pixel.getRed() + pixel.getGreen() > 220*3) {
      var bgPixel = bgImage.getPixel(x, y);
      output.setPixel(x, y, bgPixel);
    }
    else {
      output.setPixel(x,y,pixel);
    }
  }
  output.drawTo(fgcan);
}

function clearCanvas(){
  var ctx = fgcan.getContext("2d");
  ctx.clearRect(0,0,fgImage.getWidth(),fgImage.getHeight());

  var ctx = bgcan.getContext("2d");
  ctx.clearRect(0,0,bgImage.getWidth(),bgImage.getHeight());
}

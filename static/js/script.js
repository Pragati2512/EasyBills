var fgImage=null, bgImage=null, composite=null, count=0, value=0, finalImage=null;

function fgUpload() {
  var file = document.getElementById("fgFile");
  fgImage = new SimpleImage(file);
  display('canvas1', fgImage);
}

function bgUpload() {
  var file = document.getElementById("bgFile");
  bgImage = new SimpleImage(file);
  display('canvas2', bgImage);
}

function createComposite() {
  fg = new SimpleImage(fgImage);
  bg = new SimpleImage(bgImage);
  
 for ( var pixel of fg.values()){
    if (pixel.getGreen() > 250){
        x = pixel.getX();
        y = pixel.getY();
        source = bg.getPixel(x,y);
        newRed  = source.getRed();
        newBlue = source.getBlue();
        newGreen = source.getGreen();
        
        pixel.setRed(newRed);
        pixel.setBlue(newBlue);
        pixel.setGreen(newGreen);
    }
}
  composite = fg;
  display('canvas1', composite);
  clear('canvas2');
}

function display(id, img) {
  var image = img
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0, canvas.width, canvas.height);
  image.drawTo(canvas);
}

function clear(id) {
  var canvas = document.getElementById(id);
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0,0, canvas.width, canvas.height);
}

function clearCanvases() {
  clear('canvas1');
  clear('canvas2');
}

function assignValue(val) {
  value = val;
}

function applyfilter() {
  if (value==1) {
    filterGray();
  }
  else if (value == 2) {
    filterRainbow();
  }
  else if (value == 3) {
    filterBlur();
  }
  display('canvas2', finalImage);
}

function filterGray() {
  var GrayImage = new SimpleImage(fgImage);
  for ( var pixel of GrayImage.values()){
    var avg  = (pixel.getRed()+pixel.getBlue() + pixel.getGreen())/3;

    pixel.setRed(avg);
    pixel.setBlue(avg);
    pixel.setGreen(avg);
  }
  finalImage = GrayImage;
}


function filterRainbow() {
  var RainbowImage = new SimpleImage(fgImage);
  w = (RainbowImage.getWidth())/3;

  for( var pixel of RainbowImage.values()) {
    x = pixel.getX();
    if(x < w)
      pixel.setRed(255);

    else if (x >= w && x <= 2*w)
      pixel.setGreen(255);

    else if (x > 2*w)
      pixel.setBlue(255)
  }
  finalImage = RainbowImage;
}

function filterBlur() {
  var image = new SimpleImage(fgImage);
  var output = new SimpleImage(image.getWidth(), image.getHeight());

for (var pixel of image.values()) {
    var x = pixel.getX();
    var y = pixel.getY();
    if (Math.random() > 0.5) {
        var other = getPixelNearby(image, x, y, 10);
        output.setPixel(x, y, other);
    }
    else {
        output.setPixel(x, y, pixel);
    }
}
  finalImage = output;
}

//Helper Functions for Blur Filter

function ensureInImage (coordinate, size) {
    // coordinate cannot be negative
    if (coordinate < 0) {
        return 0;
    }
    // coordinate must be in range [0 .. size-1]
    if (coordinate >= size) {
        return size - 1;
    }
    return coordinate;
}

function getPixelNearby (image, x, y, diameter) {
    var dx = Math.random() * diameter - diameter / 2;
    var dy = Math.random() * diameter - diameter / 2;
    var nx = ensureInImage(x + dx, image.getWidth());
    var ny = ensureInImage(y + dy, image.getHeight());
    return image.getPixel(nx, ny);
}

// End of Helping functions of Blur Filter
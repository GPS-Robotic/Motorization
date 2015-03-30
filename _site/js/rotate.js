/*
	2015
	Christoph Gärtner, Guan Teck Gan, Niklas Schultheiß
	Robotikpraktikum Photo Rotator

	https://github.com/Spymac/photo-rotator
*/
$.fn.rotate = function () {
	var curPos = 0;
	var initialPos = Math.abs(curPos);
	var npics = 90;
	var container = this;

	if (typeof this.attr("width") != "undefined" && typeof this.attr("height") != "undefined") {
		if (parseInt(this.attr("width")) != 0)
			var width = parseInt(this.attr("width"));
		else
			var width = 640;

		if (parseInt(this.attr("height")) != 0)
			var height = parseInt(this.attr("height"));
		else
			var height = 480;
	} else {
		var width = 640;
		var height = 480;
	}
	

	var path = this.attr("src");
	if (path.substr(-1) != '/')
		path = path + '/';

	// Preload Images
	for (var i = 0; i<npics; i++) {
		var n = ('00' + i).slice(-2);
		$('<img />').attr('src', path + "cap" + n + ".jpg").load(function() {
		   $(this).remove();
		});
	}
	var scaleImage = function (w, h) {
		width = w;
		container.css("width", w + "px");
		container.css("height", h + "px");
		container.css("background-size", w + "px " + h + "px" );
	}
	scaleImage(width, height);
	this.css("background-image","url(" + path + "cap0" + 1 + ".jpg)");

	this.mousemove(function(e){
        var x = e.pageX - this.offsetLeft;
        var perc = x/width;
        var n = Math.round(perc*89);

		n = ('00' + n).slice(-2);
      
 		container.css("background-image","url(" + path + "cap" + n + ".jpg)");
    });
	var autoplay_button = $("<button class='rotate-autoplay button'>Autoplay</button>");
	var is_playing = false;
	var playing_interval = null;

    this.after(autoplay_button);
    autoplay_button.click(function() {
    	if (!is_playing)
    	{
    		is_playing = true;
    		playing_interval = setInterval(function() {
				var n = ('00' + curPos).slice(-2);
				container.css("background-image","url(" + path + "cap" + n + ".jpg)");
				curPos++;
				if (curPos > 89)
					curPos = 0;

			}, 60);
    	}else {
	   		   		clearInterval(playing_interval);
	   		   		is_playing = false;
	   	}
    });
}
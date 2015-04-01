---
layout: post
title: "MARVON on the way to its goal!"
description: "Testing the navigation algorithm II!"
category: documentation
---

We fixed the damages caused by our crash, improved our design and took a closer look at our navigation algorithm. Furthermore we got the compass running! Now we are able to navigate via GPS and compass which makes the robots life much easier. Since this lttle breakthrough the navigation algorithm got better step by step such that we are now able to navigate through the university buildings in an area full of obstacles on small scales. Only drawback is the accuracy of our GPS module.  

##But now in more detail.
After the crash we revisited the whle robot and now it looks like this.

<div style="text-align:center"> <img src ="{{ site.baseurl }}/images/galery/new_design_III.JPG" alt="Current appearance of our car." width="60%"> </div>

<div style="text-align:center"> <img src ="{{ site.baseurl }}/images/galery/new_design_IV.JPG" alt="Current appearance of our car." width="60%"> </div>

the sensors are now shielded by metal and the GPS/compass module sits above all electrics to get better signal. Furthermore our cool looking shell is more or less finished and looks good.

<div style="text-align:center"> <img src ="{{ site.baseurl }}/images/galery/new_design_II.JPG" alt="Current appearance of our car." width="60%"> </div>

<div style="text-align:center"> <img src ="{{ site.baseurl }}/images/galery/new_design_I.jpg" alt="Current appearance of our car." width="60%"> </div>

In the last week we sat down and did one test after another to improve the navigation and to find bugs in our code or to test different ideas how to handle situations. The out come is as follows, we arte able to navigate through the corridors of our university building where every meter is an obstacle and GPS data is bad. Furthermore every ten seconds there will be a moving obstacle in form of a student :-) We didn't include moving obstacles but it kind of worked. Next time we will take a video camera and make a movie to provide you with more insights.

#MARVON rotates
As you will have recognized, thanks to our colleges from the image rotator group we have now a full 360 degree view of our robot. Isn't it cool.

<br>

<script src="https://code.jquery.com/jquery-2.1.3.min.js" type="text/javascript"></script>
<script src="{{ site.baseurl }}/js/rotate.js" type="text/javascript"></script>


</style>
</head>
<table border=0><tr><td align=center>
<body>
	<div id="image" src="{{ site.baseurl }}/images/captures/" width="640" height="480" ></div>

<script>
	$(document).ready(function() {
		$("#image").rotate();
	});
</script>
</body>
<p> Thanks to the image rotator group for this stunning 360° shot of our car! </p>
</td></tr></table>


<br>
<div  style="border-bottom: 1px solid #ddd"></div>
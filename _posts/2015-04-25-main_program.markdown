---
layout: post
title: "The main program cycle"
description: "The one loop to rule them all."
category: documentation
---

This is a brief description of our main program which we named "GPS_navigation.py" (#sudo #python).

At first the background threads for the ultrasonic sensors and the GPS module are started, the cruise control is initialized and a log-file is created. After this the main loop starts. It is repeatedly executed until the distance to the target (based on GPS data) is smaller than an estimated GPS accuracy.

The loop starts by interrogating the two fixed front sensors. When they see an obstacle, the car breaks in order not to bump into anything. Because the sensors return quite many wrong measurements, we repeat the measurement and back-off only when we really find an obstacle.

When the path is clear, the <a href="{{ site.baseurl }}/documentation/2015/04/25/obstacles_III.html">navigation function</a> takes over and returns a steering direction and a motor command (backward/ forward). After some exception handling (in cases, where no free path is found) the driving function executes the commands computed before. We chose to drive only 0.5 meter in each loop, because some crash experiences made us quiet carefull.

<div style="text-align:center"> <img src ="{{ site.baseurl }}/images/documentation/Flowchart.png" alt="One loop cycle." width="80%"> </div>



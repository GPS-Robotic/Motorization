---
layout: post
title: "Reely finds it's wheels!"
description: "First time on the road!"
category: documentation
---

After learning how to steer and how to accelerate or break it is time to see wether our car is actually able to drive. This means putting together all components (GPS, steering servo, battery, motor and raspberry), fix them onto our cool looking transparency board. 

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/appearance.jpg" alt="Current appearance of our car." align="middle" width="70%">
</td></table>

Unfortunately until now we do not have any sensors on board and we have to control our car via wireless-LAN. Nevertheless, let's go and 

# drive like crazy!

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/road.jpg" alt="Out on the road." width="70%">
</td></table>

But as for everyone the first steps are the hardest. After 1m of fun our car stopped and fun was over. Wireless-LAN connection lost and raspberry was rebooting. Checking everything led to diagnosis voltage fluctuations. Our approach using only one battery for motor and raspberry seemed not to work. So working around this issue led to two batteries, one for the motor and one for the raspberry. So we put together everything and start all over again.

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/road2.jpg" alt="Second time on the road." width="70%">
</td></table>

## Test bench

For testing minor edits on the appearance or major edits on the software we always go back to our test bench. In our case a monitor, keyboard, mouse and just a small box on a table to get the wheels up from the ground.

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/test_bench.jpg" alt="Test bench." align="middle" width="70%">
</td></table>

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/test-bench_2.jpg" alt="Test bench." align="middle" width="70%">
</td></table>

As you might have noticed, our GPS module has arrived and we are able to read in the data. So, our

## Next step

will be to implement the naviagtion algorithm and test the accuracy of the GPS module.

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/GPS.jpg" alt="The GPS modul." align="middle" width="70%">
</td></table>

Furthermore we like to add the ultrasonic sensors (untill now only 3) and test some algorithms to avoid obstacles. 

<table border="0"><td align="center">
<img src="{{ site.baseurl }}/images/documentation/sensors.jpg" alt="The supersonic sensors." align="middle" width="70%">
</td></table>

Then our goal of an autonomous car guided by GPS comes closer... 



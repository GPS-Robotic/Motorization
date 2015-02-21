---
layout: post
title: "Adding a WIFI-module to the car -- with an own Access-Point!"
description: "With a WIFI-module and an own Access-Point we can remote-control the car!"
category: documentation
---

So, 'till now we always had to connect the Raspberry Pi with a screen and keyboard to do some settings and scripting on it. This was especially annoying since the Raspi is located on our RC-car and we always had to put the hole car onto the table.
Therefore we finally managed to connect a WIFI-module with the Raspberry Pi and remote control it via SSH. As additional benefit we now are able to directly remote control the RC via SSH on the Raspi! Isn't that fun?!

Truely, it was a hard way to finally reach here. Just to tell you, why this was especially dificult:
First, we thought, we simply could plug some WLAN-module into the Raspi and connect to some network in order to be able to use SSH on another Laptop to control the Raspi remotely. Unfortunately our University is covered (only) by the Eduroam-Network, a www-accessible WIFI-Network. So this was the only candidate to connect with. So we did this only to find out, that there is no chance to connect to it via SSH from another computer: Port 22 is only opened for outgoing connections!

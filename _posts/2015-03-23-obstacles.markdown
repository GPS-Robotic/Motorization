---
layout: post
title: "MARVON finds its way!"
description: "Testing the navigation algorithm!"
category: documentation
---

This time we tested the navigation algorithm, or at least one part of it, namely the obstacle recognition. For this we had a look at this <a href="http://www.academia.edu/757737/Reactive_Navigation_Algorithm_for_Wheeled_Mobile_Robots_under_Non-Holonomic_Constraints">paper</a> and took some ideas how to process the sensor data from it.

After installing all the sensors needed we implemented the software to read out the sensor data, calculate free driving directions and recognize obstacles. But unfortunately we couldn't test our code as fats as would have liked because first we destroyed our raspberry board and had to get a new one. Finally we went outside to test our obstacle recognition and we were pretty happy that our robot seemed to drive backwards when an obstacle was recognized. This was not what we implemented, but ok. But then the problems became big ones. While testing the robot it suddenly started moving fast and hit an overhanging wall and got stuck. The sensors broke and some of our self invented mountings.

So we now spent a lot of time repairing the robot, debugging the code and reinventing better mountings to protect the sensors during a crash. Now the lab tests are doing much better and we hopefully can test obstacle recognition again tomorrow and maybe implement navigation with GPS to test it. 

Due to this many problems encountered in the last week we can't provide new pictures. But they will follow in the next days.

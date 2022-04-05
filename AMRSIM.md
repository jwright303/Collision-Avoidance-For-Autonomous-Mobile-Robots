# Point cloud object detection simulation
This is an example execution of the our simulation program which can be run on any of our datasets. This program runs our object detection algorithm first <br>
to detect all the objects in the scene, using this it then evaluates the objects based on a set of predefined rules. <br>
These rules dictate if an object is in the cameras path, and if any of the rules are violated then a collision is about to occur. <br>
At this point, the program will stop execution and display the scene in which the rule was violated. During execution, a bounding <br>
box is also displayed which represents the area that the rules are checking for violations in. <br>

Scene before collision:
<img width="680" alt="Screen Shot 2022-04-05 at 11 45 37 AM" src="https://user-images.githubusercontent.com/41707123/161827571-628ef597-bda3-40d1-8b3a-5a9b82646bef.png">

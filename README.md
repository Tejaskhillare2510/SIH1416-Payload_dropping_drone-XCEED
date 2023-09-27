
# SIH1416_Human_detection

AI based Automatic Human detection that generates an alarm and drops the payload through a Drone.



## Description

We have used a CNN based object detection model called YOLOv8. It is a long distance person detection model that succesfully detects stationary and locomotive human beings from different angles.

### Further advancements will be made which are :
1. To run the heavy AI models we can replace raspberry pi 4 with advanced circuit boards like Intel NUC and Jetson Nano.
2. Drone control to be switched between manual and auto control
3. GPS location of the destination will be fed to the drone for automatic maneuvering.
4. drone can be made fully automated by using advanced AI models in turn minimizing human interference.


## Code description 

#### Pi Stream
We are streaming the live video feed from Raspberry Pi 4 on a local host server Using pi camera library 

### ui and model
we have trained YOLOv8 model on the cloud and downloaded the weight files. The folder consist of the code for running the YOLOv8 model on the real time camera feed of the raspberry pi 4.
Also we have used streamlit library for development of the user interface and it is streamed on the local host.

### buzzer code
the folder consists of the code responsible for generation of alarm on different conditions like when the human is detected and when the payload is dropped.
## Screenshots
![image](https://github.com/Tejaskhillare2510/SIH1416-Payload_dropping_drone-XCEED/assets/122872302/4689432b-f918-4358-8b9f-8202790666c7)

![image](https://github.com/Tejaskhillare2510/SIH1416-Payload_dropping_drone-XCEED/assets/122872302/c1866a9d-b7f1-418e-b1ee-ba7c5aebf113)


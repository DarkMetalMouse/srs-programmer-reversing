# srs-programmer-reversing

This repository contains my reversing of the [REV Robotics SRS Programmer](https://www.revrobotics.com/rev-31-1108/).

I did this project because I felt the original product was lacking. I wanted to be able to precisely control the range of the servo.
You can also set closer angles than you can with the original SRS Programmer.

In [steps.txt](/steps.txt) you can find my detailed rambling during the reversing process.

## Requirements
Hardware
* A usb to serial adapter
* OR an arduino and send the packets from Serial to SoftwareSerial or Serial1 if your board supports it (See [SerialPassthrough.ino](/SerialPassthrough/SerialPassthrough.ino))
* A diode wired as shown in [cp210-wiring.png](/cp210-wiring.png) 


Software
* python
* pyserial module ```pip install pyserial```

## Usage
The programming functionality in in [programmer.py](/programmer.py)


```python ./programmer.py <COMn> <r|read> | <c|continuos> | <min angle> <max angle>```

Examples:
* Set SRS to continuos mode with usb adapter connected in COM3: ```python ./programmer.py COM3 c```

* Set SRS CCW angle from mid (left) to -10 and CW angle (right) to 100: ```python ./programmer.py COM3 -10 100```

* Read SRS configuration: ```python ./programmer.py COM3 r```
  
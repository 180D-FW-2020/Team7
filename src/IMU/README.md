# IMU - Gesture Recognition
## The IMU detects whether the user has crossed certain thresholds in acceleration and rotation
## to determine the user's inputted move. Sends messages on a 5s timer to account for
## network latency in video processing.

##Setup

Install the necessary components
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python-smbus python3-smbus # can be replaced by smbus2 library
$ conda upgrade conda
$ conda update conda
$ pip install --upgrade pip
$ sudo apt-get install git i2c-tools libi2c-dev
$ conda install -c conda-forge smbus2
```

Try opening the blacklist file:
```
$ sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
If the file is empty or it does not exist, you can keep going. Otherwise, if there is the line
blacklist i2c-bcm2708, put a ‘#’ in front to comment this line out.

Add the two lines into `/etc/modules` using a text editor
```
i2c-dev
i2c-bcm2708
```

Add the two lines into `boot/config.txt`
```
dtparam=i2c_arm=on
dtparam=i2c1=on
```

Reboot your Raspberry Pi
```
$ sudo reboot -h now
```

IMU setup complete.

## IMU Usage

To run, use the command
> python playerIMU.py --player <playerID> [<debug <DEBUG>]


Hold the IMU in your fist such that the x-axis is parallel to your extended arm
(ie, the z-axis is normal to the back of your hand).


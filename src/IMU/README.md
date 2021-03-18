# IMU - Gesture Recognition #
## The IMU detects whether the user has crossed certain thresholds in acceleration and rotation
 to determine the user's inputted move. Sends messages on a 5s timer to account for
 network latency in video processing. ##

## Dependencies ##
See requirements.txt

## IMU Usage ##

To run, use the command

`python playerIMU.py --player <playerID> [debug <DEBUG>]`

where the flag <playerID> should be populated by the value 1/2 (according to player number)
and where the flag <DEBUG> should only be set True if the player wants to see data output.

Hold the IMU in your fist such that the x-axis is parallel to your extended arm
(ie, the z-axis is normal to the back of your hand).

Threshold values can be changed within the code if necessary.

## Sources ##
* Machine learning feature extraction, model generation, etc. based on [Jennifer Wang's Gesture Recognition Magic Wand](https://github.com/jewang/gesture-demo)
* IMU libraries from [Ozzmaker](https://github.com/ozzmaker/BerryIMU)

# Code Breakdown
| File | Description |
| :---: | :--- |
| `models` | Models generated with machine learning, based on jewang notebook (liear support vector classifier). |
| `collect_data.py` | Read fixed duration of raw data from IMU and pass into .csv files. Runs continuously until command to stop given. |
| `playerIMU.py` | Connects to the client and runs the gesture classification code. |
| `modelGen.py` | Code used in Jupyter Notebook to generate data for model. |
| `README.md` | This file with usage and documentation. |
| `LIS3MDL.py`, `LSM6DSL.py`,`LSM9DS0.py`,`LSM9DS1.py` | Register addresses for individual sensors. |
| `IMU.py` | Functions to interface with IMU sensor(s). |
| `datacollection.py` | Deprecated. Collects raw and filtered data continuously. |
| `adafruit_lsm9ds1.py` | Deprecated. Somewhat equivalent to `playerIMU.py`, although not as progressed. Only works for LSM9DS1 IMU. |

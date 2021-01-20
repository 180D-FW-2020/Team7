Gesture recognition -- uses moving average filter, runs thresholding based on acceleration in normal vector to fist. Time lockout between punch states. 

## Dependencies
```
- smbus  
```
## In the pipeworks
1. Will rewrite such that it uses the BerryIMU/Ozzmaker libraries. BerryIMU v2 uses LSM9DS1, so I can incorporate that library. Potentially incorporate a 2-pole switch to choose which library to use for IMU (v3 uses LSM6DSL + LIS3MDL).
2. Adjust moving average window size with potentiometer. Unfortunately the RPi has no ADC so I will have to figure out something.
3. Gravity compensated measurements for acceleration using quaternions.
4. (Long-shot) Machine learning incorporation to classify moves dynamically.

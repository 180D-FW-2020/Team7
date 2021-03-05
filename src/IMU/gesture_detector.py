from os.path import curdir
import sys
import os
import IMU
import datetime
from pandas import DataFrame 
import utils
from joblib import load 

model = load(os.path.join(curdir, 'models', '193pt_model.joblib')) 


CHECK_TIME_INCREMENT_MS = 200
SAMPLE_SIZE_MS = 1500

_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700    




class gestureRecognizer: 

    def __init__(self): 
        global SAMPLE_SIZE_MS

        IMU.detectIMU()     #Detect if BerryIMU is connected.
        if(IMU.BerryIMUversion == 99):
            print(" No BerryIMU found... exiting ")
            sys.exit()
        IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

        print('Starting operation')

        self.i = 0
        self.header = ["time_ms", "delta_ms"] + utils.get_sensor_headers()
        self.data = [] 
        self.maxlen = int(SAMPLE_SIZE_MS / 10)
        self.start = datetime.datetime.now()
        self.elapsed_ms = 0
        self.previous_elapsed_ms = 0
        self.last_classified = 0
        self.last_classification = "negative_trim"

    def collect(self): 

        #Read the accelerometer,gyroscope and magnetometer values
        aX = IMU.readACCx(); aY = IMU.readACCy(); aZ = IMU.readACCz()
        gX = IMU.readGYRx(); gY = IMU.readGYRy(); gZ = IMU.readGYRz()
        MAGx = IMU.readMAGx(); MAGy = IMU.readMAGy(); MAGz = IMU.readMAGz()
        
        accel = [aX, aY, aZ]
        mag = [MAGx, MAGy, MAGz] 
        gyro = [gX, gY, gZ]
        euler = [0, 0, 0]
        quaternion = [0, 0, 0, 0]
        lin_accel = [0, 0, 0]
        gravity = [0, 0, 0]

        return accel + mag + gyro + euler + quaternion + lin_accel + gravity 

    def classify(self): 
        global model, CHECK_TIME_INCREMENT_MS

        while True: 
            row = [self.elapsed_ms, int(self.elapsed_ms - self.previous_elapsed_ms)] + self.collect()
            self.data.append(row)
            self.previous_elapsed_ms = self.elapsed_ms

            if self.elapsed_ms - self.last_classified >= CHECK_TIME_INCREMENT_MS and len(self.data) == self.maxlen:
                df = DataFrame(list(self.data), columns=self.header)
                features = utils.get_model_features(df) + [0]
                # for i in features: 
                #     print(i)
                prediction = model.predict([features])[0]

                #print(int(elapsed_ms), prediction)
                if prediction != 'negative_trim' and self.last_classification != prediction:
                    print("========================>", prediction)
                
                self.data.clear()

                self.last_classified = self.elapsed_ms
                self.last_classification = prediction 
                
                break 

            self.elapsed_ms = (datetime.datetime.now() - self.start).total_seconds() * 1000

        return str(self.last_classification)
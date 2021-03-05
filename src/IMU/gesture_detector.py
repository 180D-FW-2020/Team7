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

    def get_sensor_headers(self):
        header = []
        for sensor in ["accel_ms2", "mag_uT", "gyro_degs", "euler_deg",
                    "quaternion",
                    "lin_accel_ms2", "gravity_ms2"]:
            if sensor is "quaternion":
                header.append(sensor + "_w")
            header.append(sensor + "_x")
            header.append(sensor + "_y")
            header.append(sensor + "_z")
        return header

    def classify(self): 
        global model, CHECK_TIME_INCREMENT_MS
        data = []
        frame = {}

        while True: 
            row = [self.elapsed_ms, int(self.elapsed_ms - self.previous_elapsed_ms)] + self.collect()
            data.append(row)
            self.previous_elapsed_ms = self.elapsed_ms

            if self.elapsed_ms - self.last_classified >= CHECK_TIME_INCREMENT_MS and len(data) == self.maxlen:
                
                for x in range(len(self.header)):
                    col = []
                    for y in range(len(self.data)):
                        column.append(data[x][y])
                    frame[self.header[x]] = np.array(column)


                features = self.get_model_features(df) + [0]
                prediction = self.model.predict([features])[0]

                #print(int(elapsed_ms), prediction)
                if prediction != 'negative_trim' and self.last_classification != prediction:
                    print("========================>", prediction)
                

                self.last_classified = self.elapsed_ms
                self.last_classification = prediction 
                
                break 

            self.elapsed_ms = (datetime.datetime.now() - self.start).total_seconds() * 1000

        return str(self.last_classification)

    def get_model_features(self, trace, generate_feature_names=False):
        features = []
        trace["accel"] = np.linalg.norm(
            (trace["aX"], trace["aY"], trace["aZ"]),
            axis=0)
        trace["gyro"] = np.linalg.norm(
            (trace['gX'], trace['gY'], trace['gZ']),
            axis=0)

        for sensor in ['accel', 'gyro']:
            features_temp = self.get_features(trace[sensor], generate_feature_names)
            if generate_feature_names:
                features.extend([x + '_' + sensor for x in features_temp])
            else:
                features.extend(features_temp)

        if generate_feature_names:
            features.append('accel_z_peaks')
        else:
            normalized = self.min_max_scaler.fit_transform(
                trace['aZ'].reshape(-1, 1).astype(np.float))[:, 0]  # normalize
            normalized = normalized[0:len(normalized):5]  # subsample
            normalized = np.diff(
                (normalized > 0.77).astype(int))  # convert to binary classifier
            normalized = normalized[normalized > 0]
            features.append(sum(normalized))
            normalized = self.min_max_scaler.fit_transform(
                trace['gZ'].reshape(-1, 1).astype(np.float))[:, 0]  # normalize
            normalized = normalized[0:len(normalized):5]  # subsample
            normalized = np.diff(
                (normalized > 0.77).astype(int))  # convert to binary classifier
            normalized = normalized[normalized > 0]
            features.append(sum(normalized))

        return features

    def get_features(self, series, generate_feature_names=False):
        if generate_feature_names:
            return ['max', 'min', 'range', 'mean', 'std']
        features = []
        features.extend((max(series), min(series), max(series) - min(series), series.mean(), series.std()))
        return features
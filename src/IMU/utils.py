import numpy as np
import pandas as pd
from sklearn import preprocessing

min_max_scaler = preprocessing.MinMaxScaler()

QUATERNION_SCALE = (1.0 / (1 << 14))


def get_features(series, generate_feature_names=False):
    if generate_feature_names:
        return ['max', 'min', 'range', 'mean', 'std']
    features = []
    features.append(max(series))
    features.append(min(series))
    features.append(max(series) - min(series))
    features.append(series.mean())
    features.append(series.std())
    return features


def get_model_features(trace, generate_feature_names=False):
    features = []
    trace["accel"] = np.linalg.norm(
        (trace["aX"], trace["aY"], trace["aZ"]),
        axis=0)
    trace["gyro"] = np.linalg.norm(
        (trace['gX'], trace['gY'], trace['gZ']),
        axis=0)

    for sensor in ['accel', 'gyro']:
        features_temp = get_features(trace[sensor], generate_feature_names)
        if generate_feature_names:
            features.extend([x + '_' + sensor for x in features_temp])
        else:
            features.extend(features_temp)

    if generate_feature_names:
        features.append('accel_z_peaks')
    else:
        normalized = min_max_scaler.fit_transform(
            trace['aZ'].values.reshape(-1, 1))[:, 0]  # normalize
        normalized = normalized[0:len(normalized):5]  # subsample
        normalized = np.diff(
            (normalized > 0.77).astype(int))  # convert to binary classifier
        normalized = normalized[normalized > 0]
        features.append(sum(normalized))

    return features


def get_sensor_headers():
    header = []
    for sensor in ["a", "m", "g", "euler_deg",
                   "quaternion",
                   "lin_accel_ms2", "gravity_ms2"]:
        if sensor is "quaternion":
            header.append(sensor + "W")
        header.append(sensor + "X")
        header.append(sensor + "Y")
        header.append(sensor + "Z")
    return header

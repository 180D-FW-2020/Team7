#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install plotly==4.14.3 chart_studio cufflinks pandas joblib')


# In[17]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import plotly

import chart_studio.plotly as py
from  plotly.offline import iplot
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)
import cufflinks as cf
cf.go_offline()

import pandas as pd
import numpy as np
import glob
import random
from sklearn import preprocessing

# Make sure we are running Python 3
import sys
print(sys.version)


# In[40]:


FOLDER_NAMES = ["cross", "hook", "negative"]
GESTURES = ["cross", "hook", "negative_trim"]

# Manually determined trims (copied from Google Sheets)
TRIMS = pd.read_csv('trim_ms.csv', header=0, index_col=0, squeeze=True)
TRIMS = pd.to_numeric(TRIMS, errors='coerce').to_dict()

SEGMENT_LEN_MS = 1490
SAMPLE_FREQ_HZ = 120
SEGMENT_LEN = int(SEGMENT_LEN_MS / SAMPLE_FREQ_HZ * 10) - 5


# In[41]:


min_max_scaler = preprocessing.MinMaxScaler()

def read_data(folder_name):
    traces = []
    trace_names = []
    for f in sorted(glob.glob(folder_name + "/*.csv")):
        print(f)
        filename = f[f.find('/') + 1:-4]
        trace = pd.read_csv(f, header=0, index_col="time_ms")
        print(trace.shape)
        trace = trace.apply(pd.to_numeric, errors='coerce')
        trace["accel"] = np.linalg.norm((trace["aX"], trace["aY"], trace["aZ"]), axis=0)
        trace["gyro"] = np.linalg.norm((trace["gX"], trace["gY"], trace["gZ"]), axis=0)
        
        
        normalized = min_max_scaler.fit_transform(trace['aZ'].values.reshape(-1, 1))
        normalized = normalized[:, 0]
        trace["normalized_accel_z"] = normalized
        
        trace_names.append(filename)
        traces.append(trace)
    return trace_names, traces
        
traces = {}
trace_names = {}
for folder_name in FOLDER_NAMES:
    trace_names[folder_name], traces[folder_name] = read_data(folder_name)


# In[42]:


# Split the long negative traces in 1.5 second segments
traces["negative_trim"] = []
trace_names["negative_trim"] = []
for i, trace in enumerate(traces["negative"]):
    for j in range(0, len(trace), 500):
        # Pad an extra 10 to make sure are generous with data points
        traces["negative_trim"].append(trace[j:j + SEGMENT_LEN_MS + 10])
        trace_names["negative_trim"].append(trace_names["negative"][i] + '_' + str(j))


# In[43]:


# Trim traces
for gesture in GESTURES:
    for i, trace in enumerate(traces[gesture]):
        filename = trace_names[gesture][i]
        
        if filename in TRIMS:
            trim = TRIMS[filename]  
            if np.isnan(trim) or trim < SEGMENT_LEN_MS:
                print('DROPPING TRACE', filename, 'TRIM IS TOO EARLY / BLACKLISTED')
                del traces[gesture][i]
                del trace_names[gesture][i]
                continue
            trim += random.randrange(0, 200)
            trace = trace[trim - SEGMENT_LEN_MS:trim]
            
        if len(trace) < SEGMENT_LEN:
            print('DROPPING TRACE', filename, 'NOT ENOUGH DATA POINTS')
            del traces[gesture][i]
            del trace_names[gesture][i]
            continue
            
        traces[gesture][i] = trace.iloc[len(trace) - SEGMENT_LEN:]
        print(filename)
        trace.index = trace.index - trace.index[0]
        traces[gesture][i] = trace


# In[44]:


print(traces["cross"][0].columns)


# In[45]:


SENSORS_LIST = ["aX", "aY", "aZ"]
# SENSORS_LIST = ["gyro_degs_x", "gyro_degs_y", "gyro_degs_z"]
# SENSORS_LIST = ["accel"]
SENSORS_LIST = ["normalized_accel_z"]
def plot_all(gesture, large=False):
    for i, trace in enumerate(traces[gesture]):
        data = [] 
        annotations = []
        for sensor in SENSORS_LIST:
            data.append(go.Scatter(
                x = trace.index,
                y = trace[sensor],
                name = sensor,
                line = dict(width = 4 if large else 1)))
            
#             annotations.append(dict(xref='paper', x=1, y=trace[sensor].iloc[-1],
#                                   xanchor='left', yanchor='middle',
#                                   text=sensor,
#                                   showarrow=False))
        layout = go.Layout(
            title = trace_names[gesture][i],
            annotations = annotations,
            font=dict(size=28 if large else 8),
            width=1000,
            margin=go.layout.Margin(r=200, pad=5),
            xaxis = dict(title='Time (ms)'))
            #showlegend=False,
            #yaxis = dict(range=[0, 25])
            #              )
        iplot({'data': data, 'layout': layout}, filename='jupyter-basic_bar')


# In[11]:


#plot_all("cross")


# In[46]:


import utils

print(utils)

def get_all_features(trace, generate_feature_names=False):
    features = utils.get_model_features(trace, generate_feature_names)
    
    if generate_feature_names:
        features.append('accel_z_peaks')
    else:
        normalized = min_max_scaler.fit_transform(trace['normalized_accel_z'].values.reshape(-1, 1))[:, 0] # normalize
        normalized = normalized[0:len(normalized):5] # subsample
        normalized = np.diff((normalized > 0.77).astype(int)) # convert to binary classifier
        normalized = normalized[normalized>0]
        features.append(sum(normalized))
    
    return features


# In[47]:


# # Sandbox for developing new features

import scipy.fftpack
import matplotlib.pyplot as plot

d = {'cross': [], 'hook': []}
for gesture in d.keys():
    for trace in traces[gesture]:
        normalized = min_max_scaler.fit_transform(trace['normalized_accel_z'].values.reshape(-1, 1))
        normalized = normalized[:, 0]
        normalized = normalized[0:len(normalized):5]
        normalized = np.diff((normalized > 0.77).astype(int))
        normalized = normalized[normalized>0]
        d[gesture].append(sum(normalized))

    viz = pd.Series(d[gesture])
    if gesture is 'cross':
        print('cross peak count accuracy', float(len(viz[viz == 2])) / len(viz))
    else: 
        print('hook peak count accuracy', float(len(viz[viz == 3])) / len(viz))
        
    plot.hist(d[gesture],density=1, bins=20) 
    plot.show()


# In[48]:


# Feature Extraction

Y = GESTURES[:]
X = []
FEATURE_NAMES = []
AVG_X = []

for gesture in GESTURES:
    samples = []
    sum_samples = []
    for trace in traces[gesture]:
        if not FEATURE_NAMES:
            FEATURE_NAMES = get_all_features(trace, True)
    
        feature_values = get_all_features(trace)
        
        if not sum_samples:
            sum_samples = feature_values[:]
        else:
            sum_samples = [sum_samples[i] + feature_values[i] for i in range(len(feature_values))]
        samples.append(feature_values)
        
    AVG_X.append([x / float(len(traces[gesture])) for x in sum_samples])
    X.append(samples)


# In[49]:


average_sample = pd.DataFrame(AVG_X, Y, columns=FEATURE_NAMES).transpose()
display(average_sample)
average_sample.iplot()


# In[50]:


for gesture in GESTURES:
    print(gesture, len(traces[gesture]))
    
from sklearn.model_selection import train_test_split

# Flatten the data
X_flat = []
y_flat = []
for i in range(len(X)):
    X_flat += X[i]
    y_flat += [GESTURES[i]] * len(X[i])
X_flat = np.array(X_flat)
y_flat = np.array(y_flat)

# Generate pretty table of all for display
pretty_table = pd.DataFrame(X_flat, columns=FEATURE_NAMES)
pretty_table['y'] = pd.DataFrame(y_flat)
# display(pretty_table)

# Split into training and test set
X_train, X_test, y_train, y_test = train_test_split(X_flat, y_flat, test_size=0.33, random_state=42)
print(X_train.shape)
# print(y_train)
print(X_test.shape)
# print(y_test)


# In[51]:


# Linear SVC Model

# Actually train the model
from sklearn import svm
from sklearn.metrics import confusion_matrix
model = svm.LinearSVC(max_iter=100000)
model.fit(X_train, y_train) 

# How did we do? 
print("Score:", model.score(X_test, y_test))
predictions = model.predict(X_test)
display(confusion_matrix(y_test, predictions))
df = pd.concat([pd.Series(predictions), pd.Series(y_test)], axis=1)
df.columns=["predicted", "actual"]
display(df)

# Save the model
import joblib
joblib.dump(model, 'models/' + str(len(X_flat)) + 'pt_model.joblib') 


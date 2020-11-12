import csv
import time
import board
import busio
import adafruit_lsm9ds1


header = ["time","accX","accY","accZ","gyroX","gyroY","gyroZ","temp"]
with open("{}.csv".format(time.strftime('%Y%m%d-%H%M%S'), 'w')) as csvfile:
    i2c = busio.I2C(board.SCL, board.SDA)
    s = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    t = time.time()
    while 1:
        buffer = [time.time - t]
        buffer.extend(s.acceleration)
        buffer.extend(s.gyro)
        buffer.append(s.temperature)
        csvwriter.writerow(buffer)
#!/usr/bin/env python
# encoding: utf-8


import serial
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from collections import deque

app = QtGui.QApplication([])

port, baud = '/dev/ttyACM0', 1000000

ser = serial.Serial(port, baud)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')


#BUF_SIZE = 500
BUF_SIZE = 5000

px = win.addPlot(title="Axis X")
xcurve = px.plot(pen='y')

win.nextRow()

py = win.addPlot(title="Axis Y")
ycurve = py.plot(pen='y')

win.nextRow()

pz = win.addPlot(title="Axis Z")
zcurve = pz.plot(pen='y')

xdata = deque(np.zeros(BUF_SIZE), maxlen=BUF_SIZE)
ydata = deque(np.zeros(BUF_SIZE), maxlen=BUF_SIZE)
zdata = deque(np.zeros(BUF_SIZE), maxlen=BUF_SIZE)

tstamp = deque(np.arange(BUF_SIZE), maxlen=BUF_SIZE)

px.enableAutoRange('y', True)
py.enableAutoRange('y', True)
pz.enableAutoRange('y', True)

#px.setYRange(-28,28)
#py.setYRange(-28,28)
#pz.setYRange(-28,28)

px.setMouseEnabled(x=False, y=True)
py.setMouseEnabled(x=False, y=True)
pz.setMouseEnabled(x=False, y=True)

def read_data():
    raw = ser.readline().strip()
    try:
        #gx,gy,gz,ax,ay,az = map(lambda x: int(x.strip()), raw.split())
        new_data = map(lambda x: int(x.strip()), raw.split())
        gx,gy,gz = new_data[0], new_data[1], new_data[3]

        xdata.append(gx)
        ydata.append(gy)
        zdata.append(gz)
        tstamp.append(tstamp[-1]+1)
    except KeyboardInterrupt:
        raise
    except StandardError as e:
        print e
        print raw

def update():
    global curve, data
    xcurve.setData(tstamp, xdata)
    ycurve.setData(tstamp, ydata)
    zcurve.setData(tstamp, zdata)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

timer2 = QtCore.QTimer()
timer2.timeout.connect(read_data)
timer2.start(1)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()


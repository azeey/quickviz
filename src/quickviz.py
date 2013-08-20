# -*- coding: utf-8 -*-
"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

import serial
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from collections import deque

app = QtGui.QApplication([])

ser = serial.Serial('/dev/ttyACM0', 9600)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')


BUF_SIZE = 1000

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

tstamp = deque(np.zeros(BUF_SIZE), maxlen=BUF_SIZE)

px.enableAutoRange('y', False)  ## stop auto-scaling after the first data set is plotted
py.enableAutoRange('y', False)  ## stop auto-scaling after the first data set is plotted
pz.enableAutoRange('y', False)  ## stop auto-scaling after the first data set is plotted

px.setYRange(-28,28)
py.setYRange(-28,28)
pz.setYRange(-28,28)

def read_data():
    raw = ser.readline().strip()
    try:
        x,y,z = map(int, raw.split(','))
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)
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
timer.start(100)

timer2 = QtCore.QTimer()
timer2.timeout.connect(read_data)
timer2.start(1)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()


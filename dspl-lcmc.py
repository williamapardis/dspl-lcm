

# dependencies
import time
import numpy as np
import argparse
# PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
# lcmtypes
import lcm
from lcmtypes.dspl import dspl_t


# lcm handler
lc = lcm.LCM()
# lcm class
msg = dspl_t()

# default values of lcm and dspl lights
msg.channelMode = 1
# msg.temperature = float(np.random.uniform(4.1,33.5))
# msg.humidity = float(np.random.uniform(10.5,95.2))
msg.lightLevel = 25
# msg.secsSinceComs = float(10)
# msg.nackCount = float(2)


# input arguments
parser = argparse.ArgumentParser(description='Controls the DSPL lights on mesobot.')
parser.add_argument('light', type=str)
args = parser.parse_args()
light = args.light

# message publishing logic
def pubMsg():
    if(light=="upper"):
        print("commanding the upper light...")
        lc.publish(light, msg.encode())
    elif(light=="lower"):
        lc.publish(light, msg.encode())
        print("commanding the lower light...")
    elif(light=="both"):
        lc.publish("upper", msg.encode())
        lc.publish("lower", msg.encode())
        print("commanding both lights...")
    else:
        print("error, please input lower, upper or both")
        exit()

# init default values
pubMsg()


##  APPLICATION CREATION ##
# layout 
app = QApplication([])
app.setApplicationName(light+" DSPL Control")
window = QWidget()
window.setGeometry(0,0,300,100)
# center UI
rect = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
rect.moveCenter(centerPoint)
window.move(rect.topLeft())
# generic layout
layout = QVBoxLayout()


## WIGETS ##
# on/off select combo box 
togON = QComboBox()
togON.addItems(['OFF','ON'])
# callback for toggle currentIndex conviently matched with just the addition of 1
def toggleChg():
    print(togON.currentIndex())
    print(togON.currentText())
togON.currentIndexChanged.connect(toggleChg)
layout.addWidget(togON,1)

# channel color select combo box
toggle = QComboBox()
toggle.addItems(['White','Red'])
# callback for toggle currentIndex conviently matched with just the addition of 1
def toggleChg():
    msg.channelMode = toggle.currentIndex()+1
    msg.utime = int(time.time() * 1000000)
    pubMsg()
    print(toggle.currentText())
toggle.currentIndexChanged.connect(toggleChg)
layout.addWidget(toggle,1)

# Intensity input spinner
spin = QSpinBox()
layout.addWidget(spin,1)
spin.setValue(msg.lightLevel)
spin.setRange(0,100)
spin.setAlignment(Qt.AlignCenter)
# spinner callback function
def valuechange(self):
    msg.lightLevel = spin.value()
    msg.utime = int(time.time() * 1000000)
    pubMsg()
    print('light level set to %s' % msg.lightLevel)
# connect callback function to spinner    
spin.valueChanged.connect(valuechange)



window.setLayout(layout)
window.show()
app.exec()

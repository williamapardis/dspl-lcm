

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

# application creation and layout 
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



# button creation
whiteB = QPushButton('White')
redB   = QPushButton('Red')
layout.addWidget(whiteB,1)
layout.addWidget(redB,1)
# button callback function
def clicked(value):
    msg.channelMode = value
    msg.utime = int(time.time() * 1000000)
    pubMsg()
    print('channel mode set to %s' % value)
    # button color logic
    if(value):
        print('white')
    else:
        print('red')
# connect callbacks to buttons
whiteB.clicked.connect(lambda: clicked(1))
redB.clicked.connect(lambda: clicked(0))
whiteB.setStyleSheet("background-color: white")
redB.setStyleSheet("background-color: red")


# Intensity input
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
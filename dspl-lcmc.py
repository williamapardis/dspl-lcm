

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
# static values of lcm
msg.temperature = float(np.random.uniform(4.1,33.5))
msg.humidity = float(np.random.uniform(10.5,95.2))
msg.lightLevel = int(np.random.uniform(0,100))
msg.secsSinceComs = float(10)
msg.nackCount = float(2)


# input arguments
parser = argparse.ArgumentParser(description='Controls the DSPL lights on mesobot.')
parser.add_argument('light', type=str)
args = parser.parse_args()
light = args.light
if(light=="upper"):
    print("commanding the upper light addr:002, ttyA3")
    msg.lightNumber = 2
elif(light=="lower"):
    print("commanding the lower light addr:003, ttyA5")
    msg.lightNumber = 3
else:
    print("error, please input lower or upper")
    exit()

# application creation and layout 
app = QApplication([])
app.setApplicationName("DSPL "+light+" Control")
window = QWidget()
window.setGeometry(0,0,300,100)
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
    lc.publish(light, msg.encode())
    print(msg)
# connect callbacks to buttons
whiteB.clicked.connect(lambda: clicked(1))
redB.clicked.connect(lambda: clicked(0))


# Intensity input
spin = QSpinBox()
layout.addWidget(spin,1)
spin.setValue(0)
spin.setRange(0,100)
spin.setAlignment(Qt.AlignCenter)
# spinner callback function
def valuechange(self):
    msg.lightLevel = spin.value()
    msg.utime = int(time.time() * 1000000)
    lc.publish(light, msg.encode())
    print(msg.lightLevel)
# connect callback function to spinner    
spin.valueChanged.connect(valuechange)

window.setLayout(layout)
window.show()
app.exec()
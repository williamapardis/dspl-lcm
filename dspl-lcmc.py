# import lcm
# import time
# import numpy as np

# from lcmtypes.dspl import dspl_t

# lc = lcm.LCM()

# msg = dspl_t()
# msg.utime = int(time.time() * 1000000)
# msg.lightNumber = 1
# msg.temperature = float(np.random.uniform(4.1,33.5))
# msg.humidity = float(np.random.uniform(10.5,95.2))
# msg.channelMode = 5
# msg.lightLevel = int(np.random.uniform(0,100))
# msg.secsSinceComs = float(10)
# msg.nackCount = float(2)

# lc.publish("EXAMPLE", msg.encode())

# dependencies
import argparse
# PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
# lcmtypes
from lcmtypes.dspl import dspl_t


parser = argparse.ArgumentParser(description='Controls the DSPL lights on mesobot.')
parser.add_argument('light', type=str)
args = parser.parse_args()
light = args.light
if(light=="upper"):
    print("commanding the upper light addr:002, ttyA3")
if(light=="lower"):
    print("commanding the lower light addr:003, ttyA5")


# application creation and layout 
app = QApplication([])
app.setApplicationName("DSPL "+light.upper()+" Control")
window = QWidget()
window.setGeometry(0,0,300,100)
layout = QVBoxLayout()
msg = dspl_t()


# button creation
whiteB = QPushButton('White')
redB   = QPushButton('Red')
layout.addWidget(whiteB,1)
layout.addWidget(redB,1)
# button callback function
def clicked(value):
    msg.lightNumber = value
    print(msg.lightNumber)
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
    print(msg.lightLevel)
# connect callback function to spinner    
spin.valueChanged.connect(valuechange)

window.setLayout(layout)
window.show()
app.exec()
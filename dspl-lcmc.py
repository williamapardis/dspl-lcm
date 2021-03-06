## DEPENDANTS ##
# general
import time
import numpy as np
import argparse
import os
# PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
# lcmtypes
import lcm
from lcmtypes.dspl import dspl_t
from lcmtypes.power import switch_t

## LCM SETUP ##
# lcm handler
lc = lcm.LCM()
# lcm class
swt = switch_t()
msg = dspl_t()
# default values of lcm and dspl lights
msg.channelMode = 1
msg.lightLevel = 25


## INPUT ARGUMENTS ##
parser = argparse.ArgumentParser(description='Controls the DSPL lights on mesobot.')
parser.add_argument('light', type=str)
args = parser.parse_args()
light = args.light


## CONTROL MESSAGING SETUP ##
def pubMsg():
    if(light=="both"):
        msg.port = 'A6'
        lc.publish("upper", msg.encode())
        msg.port = 'A3'
        lc.publish("lower", msg.encode())
        print("commanding both lights...")
    elif(light=="upper" or light=="lower"):
        lc.publish(light, msg.encode())
    else:
        print("error, please input lower, upper or both")
        exit()


## INIT DEFAULT LIGHT STATES ##
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
togOn = QComboBox()
togOn.addItems(['on','off'])
# callback for toggle currentIndex conviently matched with just the addition of 1
def stateChg():
    if(togOn.currentText()=='on'):
        msg.enabled = True
    elif(togOn.currentText()=='off'):
        msg.enabled = False
    pubMsg()
    #lightState(togON.currentText())
    print(togOn.currentIndex())
    print(togOn.currentText())
togOn.currentIndexChanged.connect(stateChg)
layout.addWidget(togOn,1)

# channel color select combo box
toggle = QComboBox()
toggle.addItems(['white','red'])
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
spin.setStyleSheet("QSpinBox {border : 2px solid green;}")
# spinner callback functions
def valueChg():
    spin.setStyleSheet("QSpinBox {border : 8px solid red;}")
def sendMsg():
    time.sleep(0.5)
    msg.lightLevel = spin.value()
    msg.utime = int(time.time() * 1000000)
    pubMsg()
    print('light level set to %s' % msg.lightLevel)
    spin.setStyleSheet("QSpinBox {border : 2px solid green;}")
# connect callback function to spinner    
spin.editingFinished.connect(sendMsg)
spin.valueChanged.connect(valueChg)


## START APPLICATION ##
window.setLayout(layout)
window.show()
app.exec()

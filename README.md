# DSPL control client and daemon mesobot development
## Description
Client and daemon LCM control of Deep Sea Power and Light [LSL-2025](https://www.deapsea.com/led-sealite/lsl-2025-multiray) for WHOI DSL's AUX/ROV Mesobot. Through dspl_t.lcm the topside control client communicates with the vehical side daemon to appropriate serial commands via raw_bytes_t.lcm to the [serial-lcm-bridge](git@github.com:whoidsl-mesobot/serial-lcm-bridge.git).  

## Required Installation
###### Dependencies
```
pip install PyQt5
```
```
pip install paramiko
```
###### Clone Repo
```
git clone git@github.com:williamapardis/mesobot.git
```
###### Cloning genaric serial lcm bridge daemon 
Intallation of generic serial lcm bridge instructions:
```
mkdir mb3
cd mb3
git clone git@github.com:whoidsl-mesobot/serial-lcm-bridge.git
```
###### Double check LCM types match
Make sure mb3/serial-lcm-bridge/lcmtypes/raw_bytes_t.lcm matches lcmtypes/raw_bytes_t.lcm

Must run daemon with TTL>0

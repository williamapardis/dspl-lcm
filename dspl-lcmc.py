import lcm
import time
import numpy as np

from lcmtypes.dspl import dspl_t

lc = lcm.LCM()

msg = dspl_t()
msg.utime = int(time.time() * 1000000)
msg.lightNumber = 1
msg.temperature = float(np.random.uniform(4.1,33.5))
msg.humidity = float(np.random.uniform(10.5,95.2))
msg.channelMode = 5
msg.lightLevel = int(np.random.uniform(0,100))
msg.secsSinceComs = float(10)
msg.nackCount = float(2)

lc.publish("EXAMPLE", msg.encode())

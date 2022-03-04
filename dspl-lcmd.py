# This example demonstrates how to use LCM with the Python select module

import select
import lcm
from lcmtypes.dspl import dspl_t

def my_handler(channel, data):
    msg = dspl_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   utime   = %s" % str(msg.utime))
    print("   lightNum    = %s" % str(msg.lightNumber))
    print("   temp = %s" % str(msg.temperature))
    print("   humidity: %s" % str(msg.humidity))
    print("   channelMode        = '%s'" % msg.channelMode)
    print("   lightLevel     = %s" % str(msg.lightLevel))
    print("")
    print("!00%s:LOUT=%s" % (str(msg.lightNumber),str(msg.lightLevel)))
    print("!00%s:CHSW=%s" % (str(msg.lightNumber),str(msg.channelMode)))
    print("")

lc = lcm.LCM()
lc.subscribe("EXAMPLE", my_handler)

try:
    timeout = 1.5  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()
        else:
            print("Waiting for message...")
except KeyboardInterrupt:
    pass

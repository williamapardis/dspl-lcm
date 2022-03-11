# dependencies
import time
import argparse
# lcm
import lcm
import select
# lcmtypes
from lcmtypes.dspl import dspl_t
from lcmtypes.raw import bytes_t

# lcm handler 
lc = lcm.LCM()

# input arguments
parser = argparse.ArgumentParser(description='Controls the DSPL lights on mesobot.')
parser.add_argument('light', type=str)
args = parser.parse_args()
light = args.light
# input conditioning
if(light=="upper"):
    waiter="listening for upper light..."
    lightNumber=2
elif(light=="lower"):
    waiter="listening for lower light..."
    lightNumber=3
else:
    print("error, please input lower or upper")
    exit()
    

# callback function for when lcm msg recieved
def my_handler(channel, data):
    msg = dspl_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   utime   = %s" % str(msg.utime))
    print("   upFlag   = %s" % str(msg.upFlag))
    print("   loFlag   = %s" % str(msg.loFlag))

    print("   temp = %s" % str(msg.temperature))
    print("   humidity: %s" % str(msg.humidity))
    print("   channelMode        = '%s'" % msg.channelMode)
    print("   lightLevel     = %s" % str(msg.lightLevel))
    
    cmd = "!00%s:LOUT=%s" %(str(lightNumber),str(msg.lightLevel))
    print("")
    print(cmd)
    print("!00%s:CHSW=%s" % (str(lightNumber),str(msg.channelMode)))
    print("")
    
    # sending cmd to serial bridge via raw_bytes_t.lcm
#     out = bytes(cmd, 'utf-8')
# 
#     msg_o = bytes_t() 
#     msg_o.utime = int(time.time()*1000000)
#     msg_o.length = len(out)
#     msg_o.data = out
# 
#     lc.publish("ttyUSB0i",msg.encode())


# subscribe to message
lc.subscribe(light, my_handler)


try:
    timeout = 1.5  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()
        else:
            print(waiter)
except KeyboardInterrupt:
    pass

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
    tty = 'ttyA6'
elif(light=="lower"):
    waiter="listening for lower light..."
    lightNumber=3
    tty = 'ttyA3'
else:
    print("error, please input lower or upper")
    exit()
    
# sending cmd to serial bridge via raw_bytes_t.lcm
def my_sender(cmd):

    out = bytes(cmd, 'utf-8')

    msg_o = bytes_t() 
    msg_o.utime = int(time.time()*1000000)
    msg_o.length = len(out)
    msg_o.data = out

    lc.publish(tty+'i',msg_o.encode())


# callback function for when lcm msg recieved
def my_handler(channel, data):
    
    # decode message     
    msg = dspl_t.decode(data)
    # display lcm message     
    print("")
    print("Received message on channel \"%s\"" % channel)
    print("   utime   = %s" % str(msg.utime))
    print("   channelMode        = '%s'" % msg.channelMode)
    print("   lightLevel     = %s" % str(msg.lightLevel))
    print("")
    # printing serial commands      
    print("Serial commands to %s" % tty+'i')
    cmd = "!00%s:LOUT=%s\r\r\n\n" %(str(lightNumber),str(msg.lightLevel))
    print("   "+cmd)
    my_sender(cmd)
    time.sleep(0.5)
    cmd = "!00%s:CHSW=%s\r\r\n\n" % (str(lightNumber),str(msg.channelMode))
    print("   "+cmd)
    my_sender(cmd)
    print("")
    

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

import stats
import gevent
#import unicorn_driver
import unicorn_mini_driver

WINDOW_SECONDS = 1
s = stats.Stats(10, WINDOW_SECONDS)

#u = unicorn_driver.UnicornDriver()
u = unicorn_mini_driver.UnicornMiniDriver()

while True:
    (net_sent, net_recv) = s.get_network("eth1")

    in_MBs = round(float(net_recv)/1024.0/float(WINDOW_SECONDS))
    out_MBs = round(float(net_sent)/1024.0/float(WINDOW_SECONDS))
    in_mbit = in_MBs*8
    out_mbit = out_MBs*8


    u.set_network(out_mbit, in_mbit)

    cpu_speed = s.get_cpu()
    u.set_cpu(cpu_speed)
    
    u.refresh()

    gevent.sleep(.1)

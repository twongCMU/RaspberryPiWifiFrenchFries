import stats
import gevent
import unicorn_driver

WINDOW_SECONDS = 1
s = stats.Stats(4, WINDOW_SECONDS)

u = unicorn_driver()

while True:
    #sysload = s.get_load()
    (net_sent, net_recv) = s.get_network("wlp2s0")
    #temperature = s.get_temperature()
    #sysmem = s.get_memory_pct()

    #print("Load: " + str(sysload))
    #print("Mem: " + str(sysmem))
    in_MBs = round(float(net_recv)/1024.0/float(WINDOW_SECONDS))
    out_MBs = round(float(net_sent)/1024.0/float(WINDOW_SECONDS))
    in_mbit = in_MBs*8
    out_mbit = out_MBs*8
    #print("Net: in=" + str(in_mbit) + " out=" + str(out_mbit))
    #print("Temp: " + str(temperature))

    u.set_network(net_sent, net_recv)
    gevent.sleep(.25)

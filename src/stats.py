import gevent
import os
import psutil
import subprocess

#INTERFACES = ["eth0", "eth1", "wlan0", "wlan1"]
INTERFACES = ["eth1"]
#INTERFACES = ["wlp2s0"]
INTERFACES_FIELDS = ["bytes_sent", "bytes_recv"]

BYTES_SENT = 0
BYTES_RECV = 1

MEM_PCT = 2

class Stats:
    def __init__(self, samples_per_second, sample_window_seconds):
        self._cpu_mhz = 0
        self._network_data = {}
        for i in INTERFACES:
            self._network_data[i] = {}
            for j in INTERFACES_FIELDS:
                self._network_data[i][j] = [0] * (sample_window_seconds * samples_per_second)

        self._samples_poll_delay_sec = 1.0/float(samples_per_second)
        self._sample_window_count = sample_window_seconds * samples_per_second

        self._event = gevent.spawn(self._update_network)

    
    def _update_network(self):
        """Update the network stats in the background
        """
        while True:
            data = psutil.cpu_freq()
            self._cpu_mhz = data.current
            data = psutil.net_io_counters(pernic=True)
            for interface in INTERFACES:
                # append new data to the end of the list
                self._network_data[interface]["bytes_sent"].append(data[interface][BYTES_SENT])
                self._network_data[interface]["bytes_recv"].append(data[interface][BYTES_RECV])

                # if the list has more data than the window we care about, drop the oldest datapoint
                # at the front of the list
                if len(self._network_data[interface]["bytes_sent"]) > self._sample_window_count:
                    self._network_data[interface]["bytes_sent"].pop(0)
                if len(self._network_data[interface]["bytes_recv"]) > self._sample_window_count:
                    self._network_data[interface]["bytes_recv"].pop(0)
            #print("XXX " + str(self._network_data))
            gevent.sleep(self._samples_poll_delay_sec)

    def get_network(self, iface):
        """
        Returns:
           tuple of sent/received bytes over the last window of time
        """
        sent = 0
        recv = 0
        recv = self._network_data[iface]["bytes_recv"][-1] - self._network_data[iface]["bytes_recv"][0]
        sent = self._network_data[iface]["bytes_sent"][-1] - self._network_data[iface]["bytes_sent"][0]
        return (sent, recv)

    def get_cpu(self):
        return self._cpu_mhz
        
    def get_memory_pct(self):
        """
        Returns:
            an integer percentage for the current memory usage
        """
        return round(psutil.virtual_memory()[MEM_PCT])

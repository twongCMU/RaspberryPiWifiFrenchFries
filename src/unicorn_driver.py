import unicornhat
import numpy as np
import math

class UnicornDriver:
    NET_IN_TENS_ROW = 3
    NET_IN_ONES_ROW = 2
    NET_OUT_TENS_ROW = 1
    NET_OUT_ONES_ROW = 0
    
    LOAD_ROW = 4
    MEMORY_ROW = 6 

    ROW_LENGTH = 8

    def __init__(self):
        unicornhat.set_layout(unicornhat.AUTO)
        unicornhat.rotation(270)
        unicornhat.clear()
        unicornhat.brightness(.5)
        width,height=unicornhat.get_shape()
        self.ROW_LENGTH = height
        self._leds = np.zeros((width,height), np.bool)

        self.prev_sent = 0
        self.prev_recv = 0

    def _set_row(self, row, how_many):
        """
        Set one row as a bar graph
        """
        #print(f"XXX setting {row} to {how_many}")
        if how_many > self.ROW_LENGTH:
            how_many = self.ROW_LENGTH

        # Set the row as a bar graph
        for i in range(self.ROW_LENGTH):
            # if we should turn on the LED and it isn't on already
            if i < how_many and not self._leds[row][i]:
                self._leds[row][i] = True
                unicornhat.set_pixel(row, i, 128, 128, 128)
            # if we should turn off the LED and it was on
            elif i >= how_many and self._leds[row][i]:
                self._leds[row][i] = False
                unicornhat.set_pixel(row, i, 0, 0, 0)
    """
    def set_load(load_val):
        self._set_row(LOAD_ROW, round(float(load_val)*float(self.ROW_LENGTH))/100.0)

    def set_memory(memory_val):
        self._set_row(MEMORY_ROW, round(float(memory_val)*float(self.ROW_LENGTH))/100.0)
    """
    def set_network(self, sent, recv):
        recv_mbps = float(recv)/1024.0
        tens_count = round(recv_mbps*float(self.ROW_LENGTH)/100.0)
        self._set_row(self.NET_IN_TENS_ROW, tens_count)
        max = self._round_up(float(recv_mbps))
        if max == 0:
            max = 1
        count = round(float(recv_mbps)*float(0.5+self.ROW_LENGTH)/float(max))
        
        #print(f"XXX bars is {tens_count} {count} for mbps {recv_mbps} with max {max}")
        self._set_row(self.NET_IN_ONES_ROW, count)

        sent_mbps = float(sent)/1024.0
        tens_count = round(sent_mbps*float(self.ROW_LENGTH)/100.0)
        self._set_row(self.NET_OUT_TENS_ROW, tens_count)
        max = self._round_up(float(sent_mbps))
        if max == 0:
            max = 1
        count = round(float(sent_mbps)*float(0.5+self.ROW_LENGTH)/float(max))
        self._set_row(self.NET_OUT_ONES_ROW, count)

        self.prev_sent = sent_mbps
        self.prev_recv = recv_mbps

    def refresh(self):
        unicornhat.show()

    def _round_up(self, val):
        return int(math.ceil(float(val)/5.0)) * 5

from unicornhatmini import UnicornHATMini
import numpy as np
import math

class UnicornMiniDriver:
    NET_IN_TENS_ROW = 1
    NET_IN_ONES_ROW = 0
    NET_OUT_TENS_ROW = 4
    NET_OUT_ONES_ROW = 3
    CPU_ROW = 6

    CPU_MIN = 600
    CPU_MAX = 1500


    def __init__(self):
        self.unicornhatmini = UnicornHATMini()
        #unicornhat.set_layout(unicornhat.AUTO)
        self.unicornhatmini.set_rotation(90)
        self.unicornhatmini.clear()
        self.unicornhatmini.set_brightness(.05)
        width,height = self.unicornhatmini.get_shape()
        self.ROW_LENGTH = height
        self._leds = np.zeros((width,height), np.bool)

        self.CPU_MHZ_PER_PIXEL = float((self.CPU_MAX-self.CPU_MIN))/float(self.ROW_LENGTH)
        self.prev_sent = 0
        self.prev_recv = 0

    def _set_row(self, row, how_many, color):
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
                self.unicornhatmini.set_pixel(row, i, color[0], color[1], color[2])
            # if we should turn off the LED and it was on
            elif i >= how_many and self._leds[row][i]:
                self._leds[row][i] = False
                self.unicornhatmini.set_pixel(row, i, 0, 0, 0)

    def set_network(self, sent, recv):
        recv_mbps = float(recv)/1024.0
        tens_count = round(recv_mbps*float(self.ROW_LENGTH)/100.0)
        self._set_row(self.NET_IN_TENS_ROW, tens_count, (255, 0 ,0))
        max = self._round_up(float(recv_mbps))
        if max == 0:
            max = 1
        count = round(float(recv_mbps)*float(0.5+self.ROW_LENGTH)/float(max))
        
        #print(f"XXX bars is {tens_count} {count} for mbps {recv_mbps} with max {max}")
        self._set_row(self.NET_IN_ONES_ROW, count, (255, 0 ,0))

        sent_mbps = float(sent)/1024.0
        tens_count = round(sent_mbps*float(self.ROW_LENGTH)/100.0)
        self._set_row(self.NET_OUT_TENS_ROW, tens_count, (0, 255, 0))
        max = self._round_up(float(sent_mbps))
        if max == 0:
            max = 1
        count = round(float(sent_mbps)*float(0.5+self.ROW_LENGTH)/float(max))
        self._set_row(self.NET_OUT_ONES_ROW, count, (0, 255, 0))

        self.prev_sent = sent_mbps
        self.prev_recv = recv_mbps

    def set_cpu(self, cpu_speed):
        how_many = round(float(cpu_speed - self.CPU_MIN) / self.CPU_MHZ_PER_PIXEL)
        self._set_row(self.CPU_ROW, how_many, (0, 0, 255))

        
    def refresh(self):
        self.unicornhatmini.show()

    def _round_up(self, val):
        return int(math.ceil(float(val)/5.0)) * 5

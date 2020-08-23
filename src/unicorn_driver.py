import unicornhat
import numpy as np

class UnicornDriver:
    NET_IN_TENS_ROW = 0
    NET_IN_ONES_ROW = 1
    NET_OUT_TENS_ROW = 2
    NET_OUT_ONES_ROW = 3
    
    LOAD_ROW = 4
    MEMORY_ROW = 6 

    ROW_LENGTH = 8

    def __init__(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(180)
        unicornhat.clear()
        unicornhat.brightness(.2)
        width,height=unicorn.get_shape()
        ROW_LENGTH = width
        self._leds = np.zeros((width,height), np.bool)

    def _set_row(self, row, how_many):
        """
        Set one row as a bar graph
        """
        if how_many > ROW_LENGTH:
            how_many = ROW_LENGTH

        # Set the row as a bar graph
        for i in range(ROW_LENGTH):
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
        self._set_row(LOAD_ROW, round(float(load_val)*float(ROW_LENGTH))/100.0)

    def set_memory(memory_val):
        self._set_row(MEMORY_ROW, round(float(memory_val)*float(ROW_LENGTH))/100.0)
    """
    def set_network(sent, recv):
        recv_tens = float(recv)/10.0
        recv_ones = recv % 10
        self._set_row(NET_IN_TENS_ROW, round(recv_tens*float(ROW_LENGTH))/100.0)
        self._set_row(NET_IN_ONES_ROW, round(flat(recv_ones)*float(ROW_LENGTH))/100.0)

        sent_tens = float(sent)/10.0
        sent_ones = sent % 10
        self._set_row(NET_OUT_TENS_ROW, round(sent_tens*float(ROW_LENGTH))/100.0)
        self._set_row(NET_OUT_ONES_ROW, round(flat(sent_ones)*float(ROW_LENGTH))/100.0)

    def refresh(self):
        unicornhat.show()

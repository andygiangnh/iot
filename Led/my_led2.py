#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

cascaded=1
block_orientation=0
rotate=0

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
print("Created device")

def demo(n, block_orientation, rotate):
    # start demo
    msg = "Khanh An and Suri's Robot car"
    print(msg)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
    time.sleep(1)

try:
    demo(cascaded, block_orientation, rotate)
except KeyboardInterrupt:
    pass

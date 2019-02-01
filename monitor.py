#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil, re, commands, time

from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont

REFRESH_RATE = 40
NETWORK_GRAPH = []

display = InkyPHAT('yellow')
display.set_border(InkyPHAT.BLACK)

font = ImageFont.truetype('resources/OpenSans-Bold.ttf', 13)

def main():
    
    #bg = safe_image(Image.open("resources/background-3.png"))
    bg = safe_image(Image.open("resources/background-0.png"))
    canvas = ImageDraw.Draw(bg)

    CPU_TEMP = get_cpu_temp()
    NETWORK_BITES = get_network_bytes('wlan0')
    CPU_PERCENT = psutil.cpu_percent()
    MEMORY_PERCENT = psutil.virtual_memory()[2]
    UPTIME = (time.time() - psutil.boot_time()) / 60 / 60;

    try:
        DISK_PERCENT = psutil.disk_usage('/media/External Storage')[3]
    except:
        DISK_PERCENT = 0.0;

    print('CPU TEMP: %.1f*C' % CPU_TEMP)
    print('CPU USAGE: %d%%' % CPU_PERCENT)
    print('RAM USAGE: %d%%' % MEMORY_PERCENT)
    print('DISK USAGE: %.1f%%' % DISK_PERCENT)
    print('UPTIME: %d' % UPTIME)
    print('NET: IN %dmb OUT %dmb' % NETWORK_BITES)

    #NETWORK_GRAPH.append((time.time(), NETWORK_BITES))
    #print NETWORK_GRAPH

    canvas.text((160, 5), '%dh' % UPTIME, InkyPHAT.BLACK, font=font)
    
    canvas.text((5, 5), 'CPU TEMP: %.1f*C' % CPU_TEMP, InkyPHAT.BLACK, font=font)
    canvas.text((5, 20), 'CPU USAGE: %d%%' % CPU_PERCENT, InkyPHAT.BLACK, font=font)
    canvas.text((5, 35), 'RAM USAGE: %d%%' % MEMORY_PERCENT, InkyPHAT.BLACK, font=font)
    canvas.text((5, 50), 'DISK USAGE: %.1f%%' % DISK_PERCENT, InkyPHAT.BLACK, font=font)
    canvas.text((5, 65), 'IN %dmb / OUT %dmb' % NETWORK_BITES, InkyPHAT.YELLOW, font=font)

    display.set_image(bg)
    display.show()

    time.sleep(REFRESH_RATE)

def safe_image(source, mask=(InkyPHAT.WHITE, InkyPHAT.BLACK, InkyPHAT.YELLOW)):
    """Create a transparency mask.
    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.
    :param mask: Optional list of Inky pHAT colours to allow.
    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))

            if p == InkyPHAT.WHITE:
                mask_image.putpixel((x, y), InkyPHAT.BLACK)
            elif p == InkyPHAT.BLACK:
                mask_image.putpixel((x, y), InkyPHAT.WHITE)
            else:
                mask_image.putpixel((x, y), 3)

    return mask_image

def get_network_bytes(interface):
    for line in open('/proc/net/dev', 'r'):
        if interface in line:

            data = line.split('%s:' % interface)[1].split()
            rx_bytes, tx_bytes = (data[0], data[8])
            
            rx_megabits = (((int(rx_bytes) * 8) / 1024) / 1024)
            tx_megabits = (((int(tx_bytes) * 8) / 1024) / 1024)

            # Recived / transmited
            return (int(rx_megabits), int(tx_megabits))

def get_cpu_temp():
    temp = None
    err, msg = commands.getstatusoutput('/opt/vc/bin/vcgencmd measure_temp')
    if not err:
        m = re.search(r'-?\d\.?\d*', msg)   # https://stackoverflow.com/a/49563120/3904031
        try:
            temp = float(m.group())
        except:
            pass
    return temp

while True:
    main()



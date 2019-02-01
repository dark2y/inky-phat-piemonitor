#!/usr/bin/env python

import inkyphat

from PIL import Image

inkyphat.set_colour('black')

inkyphat.text([0,0], 'Hello', inkyphat.BLACK)

inkyphat.show()

inkyphat.text([0,0], 'World', 3)
inkyphat.show()
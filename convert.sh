convert resources/background.png -monochrome -negate resources/background-0.png
#convert resources/background-color.png -colors 3 resources/background-3.png
#convert  resources/0.jpeg -dither None -remap resources/original.png resources/background-3.png
#convert resources/original.png -colors 3 resources/background-3.png
#jp2a --size=212x104 ./download.jpeg --colors

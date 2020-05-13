#!/usr/bin/zsh
## Uses URLScan on current screen

# Remove old files
rm -f /tmp/screen*

# Find resolution of screen(s)
resolution=$(xdpyinfo | grep dimensions | awk '{print $2}')

# Take screenshot
scrot --focused --quality 100 /tmp/screen.png
# Resamples image to larger dpi
#convert -contrast -units PixelsPerInch -depth 4 /tmp/screen.png -resample 300 /tmp/screen.png
convert -units PixelsPerInch -resample 350 /tmp/screen.png /tmp/screen.png

## Train tesseract with https://ocr7.com
## Move .traineddata file to /usr/share/tessdata
## Use that file by specifying the language
# OCR Image
tesseract -l SauceCodePro /tmp/screen.png /tmp/screen

# Pass text to urlscan
#urxvtc -e "zsh urlscan < /tmp/screen.txt"

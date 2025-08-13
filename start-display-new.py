"""
  Raspberry PI Zero StartUp Display für waveshare
  
  (C) by Norman Markgraf
      in 2025
      
  Release 1.0 (10. August 2025)
  Release 1.1 (12. August 2025)
  
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import socket
import epd2in13_V4

# Google DNS
dns_ip4 = "8.8.8.8"
dns_ip6 = "2001:4860:4860::8888"

# Cloudflare DNS
# dns_ip4 = "1.1.1.2"
# dns_ip6 = "2606:4700:4700::1111"


def getIP4Address(prefix = "ip4: "):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect((dns_ip4, 1))
  ip4 = s.getsockname()[0]
  s.close()
  return prefix + ip4


def getIP6Address(prefix = ""):
  s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  s.connect((dns_ip6, 1))
  ip6 =s.getsockname()[0].split(":")
  s.close()
  first = ":".join(ip6[0:4]) + ":"
  second = ":".join(ip6[4:8])
  return (prefix + first, second)


def getDateTime(prefix = "Start: "):
  return prefix + str(datetime.now())[:19]


def initDisplay():
  	epd = epd2in13_V4.EPD()
  	epd.init()
  	epd.Clear(0xFF)
    return epd  


def initFonts(lst = [15, 18, 25]):
  fonts = dict()
  for size in lst:
    fonts[size] = ImageFont.truetype('Font.ttc', size)
  return fonts


def initImage(dsp):
  return Image.new("1", (dsp.height, dsp.width), 255)


def initDraw(image):
  return ImageDraew(image)


def drawText(draw, pos, text, size=18, fonds, fill=0):
  draw(pos, text, font=fonts[size], fill)


def pushImage(dsp, image):
  	dsp.display(dsp.getbuffer(image))

  
if __name__ == '__main__':
  
  try:
    display = initDisplay()
    image = initImage(display)
    fonts = initFonts()
    draw = initDraw(image)
    
    drawText(draw, (0,3), getDateTime(), 18, fonts)

  	(first, second) = getIP6Address()
  	
  	drawText(draw, (0, 30), "ip6:", 25, fonts)
  	drawText(draw, (50, 28), first, 15, fonts)
  	drawText(draw, (50, 46), "second, 15, fonts)

    drawText(draw, (0,70), getIP4Address(), 25, fonts)
    pushImage(dsp, image)
    
  	sleep(10)
    
    
  except IOError as e:
  	exit(0)
   
  except KeyboardInterrupt:    
  	epd2in13_V4.epdconfig.module_exit(cleanup=True)
  	exit(0)

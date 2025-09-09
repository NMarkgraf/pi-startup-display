"""
  Raspberry PI Zero StartUp Display für waveshare
  
  (C) by Norman Markgraf
      in 2025
      
  Release 1.0 (10. August 2025)
  Release 1.1 (12. August 2025)
  Release 1.2 ( 9. September 2025)
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import socket
import epd2in13_V4
import logging

# Logger einrichten
logger = logging.getLogger(__name__)

# Google DNS, Cloudflare DNS
dns_ip4 = ["8.8.8.8", "1.1.1.2"]
dns_ip6 = ["2001:4860:4860::8888", "2606:4700:4700::1111"]


def getIP4Address(prefix = "ip4: "):
  ip4 = None
  for dns_lookup in dns_ip4:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((dns_lookup, 1))
    if not ip4:
      ip4 = s.getsockname()[0]
    s.close()
  return prefix + ip4


def getIP6Address(prefix = ""):
  ip6 = None
  for dns_lookup in dns_ip6:
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.connect((dns_lookup, 1))
    if not ip6:
      ip6 =s.getsockname()[0].split(":")
    s.close()
  if not ip6:
      ip6 = "0000"+ 7 * ":0000"
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
  return ImageDraw.Draw(image)


def drawText(draw, pos, text, font=None, fill=0):
  if font:
    draw.text(pos, text, font=font, fill=fill)


def pushImage(dsp, image):
  dsp.display(dsp.getbuffer(image))


if __name__ == '__main__':
  logging.basicConfig(filename='start-display.log', level=logging.INFO)
  logger.info('Started at:'+getDateTime(""))
  
  try:
    display = initDisplay()
    image = initImage(display)
    fonts = initFonts()
    draw = initDraw(image)
    
    drawText(draw, (0,3), getDateTime(), fonts[18])

    logger.info('Scanning ...')
    drawText(draw, (20, 30 ), "Scanning ...", fonts[25])
    
    pushImage(display, image)
    
    sleep(30)

    while True:
      image = initImage(display)
      draw = initDraw(image)
      
      drawText(draw, (0,3), getDateTime(), fonts[18])
      
      (first, second) = getIP6Address()
      logger.info("ip6: "+ first + second)
      
      drawText(draw, (0, 30), "ip6:", fonts[25])
      drawText(draw, (50, 28), first, fonts[15])
      drawText(draw, (50, 46), second, fonts[15])
      
      ip4 = getIP4Address()
      drawText(draw, (0,70), ip4, fonts[25])
      logger.info(ip4)
      
      pushImage(display, image)
      
      sleep(100)
    
  except IOError as e:
    logger.info('Finished with IOError')
    exit(0)
   
  except KeyboardInterrupt: 
    logger.info('Finished with KeyboardInterrupt')
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit(0)
      
  logger.info('Finished')

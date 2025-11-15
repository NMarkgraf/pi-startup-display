"""
  Raspberry PI Zero StartUp Display für waveshare
  
  (C) by Norman Markgraf
      in 2025
      
  Release 1.0 (10. August 2025)
  Release 1.1 (12. August 2025)
  Release 1.2 ( 9. September 2025)
  Release 1.3 (11. September 2025)
  Release 1.4 (24. Oktober 2025)
  Release 1.5 (15. November 2025)
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import psutil
import socket
import epd2in13_V4
import logging
from systemd.journal import JournalHandler 

# Logger einrichten
logger = logging.getLogger(__name__)
logger.addHandler(JournalHandler(SYSLOG_IDENTIFIER="start-display"))

# [Google DNS, Cloudflare DNS]
dns_ip4 = ["8.8.8.8", "1.1.1.2"]
dns_ip6 = ["2001:4860:4860::8888", "2606:4700:4700::1111"]


def getAllIPAdresses():
  ip_list = []
  ip4_set = set()
  ip6_set = set()
  logger.debug(psutil.net_if_addrs())
  for interface in psutil.net_if_addrs():
    if interface != "lo":
      interface_addrs = psutil.net_if_addrs().get(interface)
      for snicaddr in interface_addrs:
          if snicaddr.family in(socket.AF_INET, socket.AF_INET6):
#              if "%" not in snicaddr.address:
            ip_list += snicaddr.address,
      for ip in ip_list:
        if ":" in ip:
          ip6_set.add(ip)
        if "." in ip:
          ip4_set.add(ip)
  logger.info(ip_list)
  logger.info(list(ip4_set))
  logger.info(list(ip6_set))
  return (list(ip4_set), list(ip6_set), ip_list)


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
  logging.basicConfig(filename='start-display.log', level=logging.DEBUG)
  logger.info('Started at '+getDateTime(""))
  counter = 0

  try:
    display = initDisplay()
    image = initImage(display)
    fonts = initFonts()
    draw = initDraw(image)
    
    drawText(draw, (0,3), getDateTime(), fonts[18])

    logger.info('Scanning ...')
    drawText(draw, (20, 30 ), "Scanning ...", fonts[25])
    
    pushImage(display, image)
    
    logger.debug('Start sleeping ...')
    sleep(20)
    logger.debug('End sleeping!')

    while True:
      image = initImage(display)
      draw = initDraw(image)
      logger.debug('draw and  image initialised!')
      
      drawText(draw, (0,3), getDateTime(), fonts[18])
      
      logger.info("Get All IP Adresses")
      (ip4_l, ip6_l, x) = getAllIPAdresses()

      ip4_len = len(ip4_l)
      ip6_len = len(ip6_l)

      if ip4_len == 0:
        ip4_l = ["0.0.0.0"]
        ip4_len = 1
        
      if ip6_len == 0:
        ip6_l = ["0:0:0:0:0:0:0:0"]
        ip6_len = 1

      max = ip4_len * ip6_len
      
      ip4 = ip4_l[counter % ip4_len]
      ip6 = ip6_l[counter % ip6_len].split(":")
      first = ":".join(ip6[0:4]) + ":"
      second = ":".join(ip6[4:8])

      logger.info("ip6: " + first + second)
      
      drawText(draw, (0, 30), "ip6:", fonts[25])
      drawText(draw, (50, 28), first, fonts[15])
      drawText(draw, (50, 46), second, fonts[15])
      
      drawText(draw, (0,70), "ip4:"+ ip4, fonts[25])
      logger.info("ip4: "+ip4)
      
      pushImage(display, image)
      
      logger.debug("Start sleeping ...")
      sleep(100)
      counter += 1
      counter %= max
      logger.debug("End sleeping!")

    
  except IOError as e:
    logger.info('Finished with IOError at '+getDateTime(""))
    exit(0)
   
  except KeyboardInterrupt: 
    logger.info('Finished with KeyboardInterrupt at '+getDateTime(""))
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit(0)
      
  logger.info('Finished at '+getDateTime(""))

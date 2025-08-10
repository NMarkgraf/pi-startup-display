"""
  Rsaspberry PI Zero StartUp Display für waveshare
  
  (C) by Norman Markgraf
      in 2025
      
  Release 1.0 (10. August 2025)
  
"""
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
import socket
import epd2in13_V4


def getIP4Address(prefix = "ip4: "):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 1)) 
  return prefix + s.getsockname()[0]


def getIP6Address(prefix = "ip6: ", hostname=""):
  try:
    addrinfo = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    for addr in addrinfo:
      if addr[0] == socket.AF_INET6:
         ip_address = addr[4][0]
         try:
            ipaddress.ip_address(ip_address) # Validiert IPv6
            return prefix + str(ip_address)
         except ValueError:
             pass  # Keine gültige IPv6-Adresse
      return prefix + "<none>" # Kein IPv6 gefunden
  except socket.gaierror:
    return prefix + "<NONE>"

def getDateTime(prefix = "Start: "):
  return prefix + str(datetime.now())

try:
	epd = epd2in13_V4.EPD()
	epd.init()
	epd.Clear(0xFF)
	font13 = ImageFont.truetype('Font.ttc', 13)
	font15 = ImageFont.truetype('Font.ttc', 15)
	font20 = ImageFont.truetype('Font.ttc', 20)
	
	image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
	
	draw = ImageDraw.Draw(image)
	draw.text((75, 0), getDateTime(), font = font13, fill = 0)
	draw.text((80,30), getIP6Address(), font = font15, fill = 0)
	draw.text((110, 60), getIP4Address(), font = font20, fill = 0)

	epd.display(epd.getbuffer(image))

except IOError as e:
	exit(0)
 
except KeyboardInterrupt:    
	epd2in13_V4.epdconfig.module_exit(cleanup=True)
	exit(0)

exit(0)

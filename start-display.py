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

# Google DNS
dns_ip4 = "8.8.8.8"
dns_ip6 = "2001:4860:4860::8888"

# Cloudflare DNS
#dns_ip4 = "1.1.1.2"
#dns_ip6 = "2606:4700:4700::1111"


def getIP4Address(prefix = "ip4: "):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect((dns_ip4, 1)) 
  return prefix + s.getsockname()[0]

def getIP6Address(prefix = ""):
  s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  s.connect((dns_ip6, 1)) 
  ip6 =s.getsockname()[0].slpit(":")
  first = ":".join(ip6[0:4]) + ":"
  second = ":".join(ip[4:8])
  return (prefix + first, second)

def getDateTime(prefix = "Start: "):
  return prefix + str(datetime.now()[:19])

try:
	epd = epd2in13_V4.EPD()
	epd.init()
	epd.Clear(0xFF)
	
	font10 = ImageFont.truetype('Font.ttc', 10)
	font13 = ImageFont.truetype('Font.ttc', 13)
	font15 = ImageFont.truetype('Font.ttc', 15)
	font20 = ImageFont.truetype('Font.ttc', 20)
	font25 = ImageFont.truetype('Font.ttc', 25)
	
	image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
	
	draw = ImageDraw.Draw(image)
	draw.text((0, 3), getDateTime(), font = font15, fill = 0)

	(first, second) = getIP6Address()
	
	draw.text((0, 30), "ip6: " + first, font = font15, fill = 0)
	draw.text((0, 48), "     " + secound, font = font15, fill = 0)

	draw.text((0, 68), getIP4Address(), font = font25, fill = 0)

	epd.display(epd.getbuffer(image))

  time.sleep(10)
  
  
except IOError as e:
	exit(0)
 
except KeyboardInterrupt:    
	epd2in13_V4.epdconfig.module_exit(cleanup=True)
	exit(0)
	
except:
  exit(0)

exit(0)

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


def getIPAddress(prefix = "ip: "):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 1)) 
  return prefix + s.getsockname()[0]

def getDateTime(prefix = "Start: "):
  return prefix + str(datetime.now())

try:
	epd = epd2in13_V4.EPD()
	epd.init()
	epd.Clear(0xFF)
	font13 = ImageFont.truetype('Font.ttc', 13)
	font15 = ImageFont.truetype('Font.ttc', 15)
	font20 = ImageFont.truetype('Font.ttc', 15)
	
	image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
	
	draw = ImageDraw.Draw(image)
	draw.text((75, 30), getDateTime(), font = font13, fill = 0)
	draw.text((120, 60), getIPAdsress(), font = font20, fill = 0)

	epd.display(epd.getbuffer(image))

except IOError as e:
	None
 
except KeyboardInterrupt:    
	epd2in13_V4.epdconfig.module_exit(cleanup=True)
	exit(0)

exit(0)

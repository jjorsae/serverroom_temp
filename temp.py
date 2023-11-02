#temp.py

import datetime
import adafruit_dht 
import board


dhtDevice = adafruit_dht.DHT22(board.D4)


temp_c=dhtDevice.temperature
humidity = dhtDevice.humidity

print("Temp: {:.1f} C  Humidity:{}%".format(temp_c,humidity))


    

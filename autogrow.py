# import standard python modules.
import time
import board
# import busio
import RPi.GPIO as GPIO
import adafruit_si7021


# Humidity
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lightpin = 12
fanpin = 16
humpin = 20
heatpin = 21
pins = [lightpin,fanpin,humpin,heatpin]
GPIO.setup(pins, GPIO.OUT)


#ADAFRUIT IO
from Adafruit_IO import Client, Feed

ADAFRUIT_IO_KEY = 'Insert Key'
ADAFRUIT_IO_USERNAME = 'Insert Username'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

temperature_feed = aio.feeds('temperature')
humidity_feed = aio.feeds('humidity')
humstate_feed = aio.feeds('humstate')
heatstate_feed = aio.feeds('heatstate')

print("\nFeeds are setup.")

# Create library object using our Bus I2C port
#i2c = busio.I2C(board.SCL, board.SDA)
#sensor = adafruit_si7021.SI7021(i2c)
sensor = adafruit_si7021.SI7021(board.I2C())

print("Si7021 Online")

while True:
    tempC = (sensor.temperature)
    temp = tempC * 9 / 5 + 32
    humidity = '%.2f'%(sensor.relative_humidity)

    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Temp: %0.1f F" % temp)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)

    aio.send(temperature_feed.key, float(temp))
    aio.send(humidity_feed.key, float(humidity))

    hum = float(humidity)
    heat = float(temp)

    if hum >= 70:
        GPIO.output(humpin, GPIO.LOW)
        print("Humidity has been turned off.")
        aio.send(humstate_feed.key, int(0))
    elif hum <= 50:
        GPIO.output(humpin, GPIO.HIGH)
        print("Humidity has been turned on.")
        aio.send(humstate_feed.key, int(1))
    elif hum > 50 and hum < 70:
        print("Humidity is in range.")
#    aio.send(humstate_feed.key, int(0))
    
    time.sleep(1)

    if heat >= 80:
        GPIO.output(heatpin, GPIO.LOW)
        print("Heater has been turned off.")
        aio.send(heatstate_feed.key, int(0))
    elif heat <= 70:
        GPIO.output(heatpin, GPIO.HIGH)
        print("Heater has been turned on.")
        aio.send(heatstate_feed.key, int(1))
    elif heat > 70 and heat < 80:
        print("Temperature is in range.")
#    aio.send(heatstate_feed.key, int(0))
    
    time.sleep(30)


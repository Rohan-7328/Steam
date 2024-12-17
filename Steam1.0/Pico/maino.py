# Afstandsensor met Neopixel code
#installeer de library: microPython


from machine import Pin
import time
import machine
import neopixel
import urequests  # HTTP library
import network    # WiFi-verbinding

# wifi instellingen via mobiele hotspot laptop
SSID = 'TwanHotspot'
PASSWORD = 'wifiyes12'
SERVER_URL = 'http://<http://127.0.0.1:5000/>:5000/update'  # Flask-endpoint

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Verbinding maken...")
while not wifi.isconnected():
    print("Nog geen verbinding...")
    time.sleep(1)
    if wifi.isconnected():
        print("WiFi verbonden!")
        print("IP-configuratie:", wifi.ifconfig())



np = neopixel.NeoPixel(machine.Pin(13), 8)
led_pins = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT),
    Pin(4, Pin.OUT)
]

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)


def measure_distance():
    start = time.ticks_us()
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)

    while echo_pin.value() == 0:
        start = time.ticks_us()
    while echo_pin.value() == 1:
        end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    distance = 0.0343 * duration / 2
    print(distance)
    return distance


#  """
#     Meet de afstand met de SR04
#  """

# implementeer deze functie

#  return 0


def display_distance(distance):
    for i in range(8):
        np[i] = [0, 0, 0]

    if distance < 80:
        np[0] = [0, 15, 0]
    if distance < 70:
        np[1] = [0, 15, 0]
    if distance < 65:
        np[2] = [0, 15, 0]
    if distance < 60:
        np[3] = [15, 15, 0]
    if distance < 57:
        np[4] = [15, 15, 0]
    if distance < 55:
        np[5] = [15, 15, 0]
    if distance < 51:
        np[6] = [15, 0, 0]
    if distance < 40:
        np[7] = [15, 0, 0]

    np.write()
    time.sleep(0.1)

    """
        Laat de afstand d.m.v. de leds zien.
        1 led =  10 cm
        2 leds = 15 cm
        3 leds = 20 cm
        4 leds = 25 cm
        5 leds = 30 cm
    """


while True:
    distance = measure_distance()
    display_distance(distance)
    time.sleep_ms(100)

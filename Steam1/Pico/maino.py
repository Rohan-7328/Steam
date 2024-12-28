# Afstandsensor met Neopixel code
#installeer de library: microPython


from machine import Pin
import time
import machine
import neopixel
import urequests  # HTTP library
import network    # WiFi-verbinding

# wifi instellingen via mobiele hotspot laptop
SSID = 'H369A7BC73E'
PASSWORD = 'C3F54E7EA52A'
url = 'http://20.151.236.255/gezondheid'  # Correct

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
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)

    #start timeout timer
    timeout_start = time.ticks_us()

    while echo_pin.value() == 0:
        if time.ticks_diff(time.ticks_us(), timeout_start) > 5000:
            print('Timeout, echo niet gestart')
            return float('inf')
    start = time.ticks_us()
    timeout_start = time.ticks_us() #reset timeout timer
    while echo_pin.value() == 1:
        if time.ticks_diff(time.ticks_us(), timeout_start) > 5000:
            print('Timeout, echo blijft hangen')
            return float('inf')
    end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    distance = 0.0343 * duration / 2
    print(distance)
    return distance

led_beeper = Pin(20, Pin.OUT)
def kleurgroen(x):
    groen = np[x] = [0, 15, 0]
    led_beeper.value(0)
    return groen

def kleurgeel(x):
    geel = np[x] = [15, 15, 0]
    led_beeper.value(0)
    return geel

def kleuroranje(x):
    oranje = np[x] = [30, 10, 0]
    led_beeper.value(0)
    return oranje

    led_beeper.value(0)
def display_distance(distance):
    for i in range(8):
        np[i] = [0, 0, 0]

    if distance > 0:
        kleurgroen(0)

    if distance < 80:
        kleurgroen(0)
    if distance < 80:
        kleurgroen(1)
    if distance < 70:
        kleurgeel(2)
    if distance < 60:
        kleurgeel(3)
    if distance < 50:
        kleuroranje(4)
    if distance < 40:
        kleuroranje(5)
    if distance < 35:
        led_beeper.value(0)
        np[6] = [15, 0, 0]
    if distance < 30:
        led_beeper.value(1)
        np[7] = [15, 0, 0]

    np.write()
    time.sleep(0.1)

# Verzoek versturen naar server
def versturen_data_afstandsensor():
    payload = {"distance": measure_distance()}
    headers = {'Content-Type': 'application/json'}
    try:
        response = urequests.post(url, json=payload, headers=headers)
        print(f"Server response: {response.text}")  # Controleer wat de server terugstuurt
        response.close()  # Sluit de respons correct om geheugen te sparen
    except Exception as e:
        print(f"Fout bij versturen van data naar server: {e}")


while True:
    distance = measure_distance()
    display_distance(distance)
    time.sleep(0.5)  # Verhoog de interval naar 1 seconde
    versturen_data_afstandsensor()

import time
import RPi.GPIO as GPIO
import spidev
import csv
from datetime import datetime

# GPIO Setup
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# SPI Setup for MCP3008 ADC
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_to_current(adc_value):
    voltage = (adc_value * 3.3) / 1023
    current = (voltage - 2.5) / 0.066
    return abs(current)

# CSV setup
csv_filename = "/home/pi/powermind_log.csv"
with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Current (A)", "Relay State"])

try:
    while True:
        adc_val = read_channel(0)
        current = convert_to_current(adc_val)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if current > 5.0:
            GPIO.output(RELAY_PIN, GPIO.LOW)
            relay_state = "OFF"
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            relay_state = "ON"

        print(f"{timestamp} | Current: {current:.2f} A | Relay: {relay_state}")

        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, round(current, 2), relay_state])

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting and cleaning up...")
    GPIO.cleanup()

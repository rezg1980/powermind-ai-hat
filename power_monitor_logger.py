
import spidev
import time
import csv
from datetime import datetime

# === CONFIGURATION ===
VREF = 5.0
ACS_OFFSET = 2.5          # ACS712 30A version voltage at 0A
ACS_SENSITIVITY = 0.066   # V per A for ACS712-30A
LOG_FILE = "power_log.csv"

# === SPI SETUP ===
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def adc_to_voltage(adc_value):
    return (adc_value / 1023.0) * VREF

def calculate_current(voltage):
    return (voltage - ACS_OFFSET) / ACS_SENSITIVITY

# === INIT CSV LOG FILE ===
with open(LOG_FILE, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Voltage (V)", "Current (A)", "Power (W)"])

# === MAIN LOOP ===
try:
    while True:
        adc_voltage = read_adc(1)  # CH1 for voltage
        adc_current = read_adc(0)  # CH0 for current

        voltage = adc_to_voltage(adc_voltage) * 5  # Scale for 0–25V sensor
        current = calculate_current(adc_to_voltage(adc_current))
        power = voltage * current

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | V: {voltage:.2f}V | I: {current:.2f}A | P: {power:.2f}W")

        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, f"{voltage:.2f}", f"{current:.2f}", f"{power:.2f}"])

        time.sleep(1)

except KeyboardInterrupt:
    spi.close()

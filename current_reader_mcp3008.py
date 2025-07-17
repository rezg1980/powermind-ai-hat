
import spidev
import time

# Constants (for ACS712 5A version; adjust if using 20A or 30A)
ACS_OFFSET = 2.5   # Voltage at 0A
ACS_SENSITIVITY = 0.185  # V per A for ACS712-5A version
VREF = 5.0

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_to_voltage(adc_value):
    return (adc_value / 1023.0) * VREF

def calculate_current(voltage):
    return (voltage - ACS_OFFSET) / ACS_SENSITIVITY

try:
    while True:
        adc_val = read_adc(0)  # CH0 for current
        voltage = convert_to_voltage(adc_val)
        current = calculate_current(voltage)
        print(f"Voltage: {voltage:.2f} V | Current: {current:.2f} A")
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()

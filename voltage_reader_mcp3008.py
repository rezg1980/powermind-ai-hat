
import spidev
import time

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_to_voltage(data, vref=5.0, scale_factor=5):
    voltage = (data * vref) / 1023
    return voltage * scale_factor  # for 0-25V sensor module

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

try:
    while True:
        adc_value = read_channel(1)  # CH1 of MCP3008
        voltage = convert_to_voltage(adc_value)
        print(f"Voltage: {voltage:.2f} V")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()

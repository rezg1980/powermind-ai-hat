
import RPi.GPIO as GPIO
import time

# === CONFIGURATION ===
RELAY_PIN = 17  # BCM numbering, change if needed

# === SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def turn_on():
    GPIO.output(RELAY_PIN, GPIO.LOW)  # LOW for active relay (depends on module)
    print("Relay ON")

def turn_off():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Relay OFF")

# === USAGE EXAMPLE ===
try:
    while True:
        turn_on()
        time.sleep(5)
        turn_off()
        time.sleep(5)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()

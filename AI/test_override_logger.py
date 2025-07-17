
from override_logger import log_override

# Simulated override events
log_override("relay_1", "ON", "User needed lights during power cut")
log_override("relay_2", "OFF", "Too much power consumption detected")
log_override("relay_3", "ON", "Override for emergency device")

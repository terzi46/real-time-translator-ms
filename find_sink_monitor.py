import sounddevice as sd
import os

print("--- Audio Devices ---")
try:
    print(sd.query_devices())
except Exception as e:
    print(f"Error querying devices: {e}")

try:
    default_input = sd.default.device[0]
    default_output = sd.default.device[1]
    print(f"Default Input Device Index: {default_input}")
    print(f"Default Output Device Index: {default_output}")
    
    dev_in = sd.query_devices(default_input)
    dev_out = sd.query_devices(default_output)
    
    print(f"Default Input Name: {dev_in['name']}")
    print(f"Default Output Name: {dev_out['name']}")

except Exception as e:
    print(f"Error getting default devices: {e}")

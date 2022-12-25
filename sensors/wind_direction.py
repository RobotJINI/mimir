from gpiozero import MCP3008
import time
adc = MCP3008(channel=0)

print(adc.value)

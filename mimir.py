from sensors.bme280_sensor import AirSensor
from sensors.ds18b20_therm import GroundSensor
from sensors.veml6070_uv import LightSensor

import time
from datetime import datetime


class Mimir:
    def __init__(self):
        self._running = True
        self._interval = 1
        
        self._air_sensor = AirSensor()
        self._ground_sensor = GroundSensor()
        self._light_sensor = LightSensor()
    
    def run(self):
        print("Running ....")
        
        while self._running:
            self._update()
            self._record()
            
            time.sleep(self._interval)
            
        print("Done!")
        
    def _update(self):
        self._air_sensor.update()
        self._ground_sensor.update()
        self._light_sensor.update()
        
    def _record(self):
        self._print_debug()
        
    def _print_debug(self):
        print(f'\nReading({datetime.now()}):')
        print(f'Temperature:{self._air_sensor.temperature}, Pressure:{self._air_sensor.pressure}, Humidity:{self._air_sensor.humidity}')
        print(f'Ground Temperature:{self._ground_sensor.temperature}')
        print(f'Reading: {self._light_sensor.uv} | Risk Level: {self._light_sensor.risk_level}')
    

def main():
    mimir = Mimir()

    mimir.run()

if __name__ == '__main__':
    main()
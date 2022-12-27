from sensors.bme280_sensor import AirSensor
from sensors.ds18b20_therm import GroundSensor
from sensors.veml6070_uv import LightSensor
from sensors.wind import WindSensor
from sensors.rain import RainSensor
from sensors.wind_direction import WindDirectionSensor

import time
from datetime import datetime
from threading import Thread


class Mimir:
    def __init__(self):
        self._running = True
        self._interval = 1
        
        self._air_sensor = AirSensor()
        self._ground_sensor = GroundSensor()
        self._light_sensor = LightSensor()
        self._wind_sensor = WindSensor()
        self._rain_sensor = RainSensor()
        self._wind_direction_sensor = WindDirectionSensor()
        
        self._wind_thread = None
        self._rain_thread = None
    
    def run(self):
        print("Running ....")
        
        self._start_sensors()
        
        while self._running:
            self._update()
            self._record()
            
            time.sleep(self._interval)
        
    def stop(self):
        print("Stopping ....")
        self._wind_sensor.stop()
        self._rain_sensor.stop()
        
        self._wind_thread.join()
        self._rain_thread.join()
        print("Done!")
        
    def _start_sensors(self):
        self._wind_thread = Thread(target=self._wind_sensor.run)
        self._wind_thread.start()
        
        self._rain_thread = Thread(target=self._rain_sensor.run)
        self._rain_thread.start()
        
    def _update(self):
        self._air_sensor.update()
        self._ground_sensor.update()
        self._light_sensor.update()
        self._wind_sensor.update()
        self._rain_sensor.update()
        self._wind_direction_sensor.update()
        
    def _record(self):
        self._print_debug()
        
    def _print_debug(self):
        print(f'\nReading({datetime.now()}):')
        print(f'Temperature:{self._air_sensor.temperature}, Pressure:{self._air_sensor.pressure}, Humidity:{self._air_sensor.humidity}')
        print(f'Ground Temperature:{self._ground_sensor.temperature}')
        print(f'UV: {self._light_sensor.uv} | Risk Level: {self._light_sensor.risk_level}')
        print(f'Wind Speed:{self._wind_sensor.wind_speed}')
        print(f'Rainfall:{self._rain_sensor.rainfall}, Rain Rate:{self._rain_sensor.rain_rate}')
        print(f'Wind Direction:{self._wind_direction_sensor.values}')
    

def main():
    mimir = Mimir()
    
    try:
        mimir.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
        
    mimir.stop()

if __name__ == '__main__':
    main()
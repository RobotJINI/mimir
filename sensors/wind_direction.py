from gpiozero import MCP3008


class WindDirectionSensor:
    def __init__(self):
        self._adc = MCP3008(channel=0)
        
        self.wind_direction = -1
        self._volts_to_degree = {0.4: 0.0,
                                 1.4: 22.5,
                                 1.2: 45.0,
                                 2.8: 67.5,
                                 2.7: 90,
                                 2.9: 112.5,
                                 2.2: 135.0,
                                 2.5: 157.5,
                                 1.8: 180.0,
                                 2.0: 202.5,
                                 0.7: 225.0,
                                 0.8: 247.5,
                                 0.1: 270.0,
                                 0.3: 292.5,
                                 0.2: 315.0,
                                 0.6: 337.5}
        self.values = []
        
    def update(self):
        
        dir_val = round(self._adc.value, 2)
        
        if dir_val not in self.values:
            self.values.append(dir_val)
        
        if dir_val in self._volts_to_degree:
            self.wind_direction = self._volts_to_degree[dir_val]

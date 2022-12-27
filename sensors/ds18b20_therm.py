#!/usr/bin/python3
import os, glob, time


class GroundSensor:
    def __init__(self, is_celsuis=False):
        self._device_file = glob.glob("/sys/bus/w1/devices/28*")[0] + "/w1_slave"
        self._is_celsuis = is_celsuis
        
        self.temperature = 0
        
    def update(self):
        temp_c = -255
        attempts = 0
        
        lines = self._read_temp_raw()
        success = self._crc_check(lines)
        
        while not success and attempts < 3:
            time.sleep(.1)
            lines = self._read_temp_raw()            
            success = self._crc_check(lines)
            attempts += 1
        
        if success:
            temp_line = lines[1]
            equal_pos = temp_line.find("t=")            
            if equal_pos != -1:
                temp_string = temp_line[equal_pos+2:]
                temp_c = float(temp_string)/1000.0
                self.temperature = temp_c if self._is_celsuis else self._convert_fahrenheit(temp_c)
        else:
            print("Error: ds18b20 failed reading.")
            
    def _read_temp_raw(self):
        f = open(self._device_file, "r")
        lines = f.readlines()
        f.close()
        return lines
    
    def _crc_check(self, lines):
        return lines[0].strip()[-3:] == "YES"
    
    def _convert_fahrenheit(self, celsuis):
        return (celsuis * 9/5) + 32

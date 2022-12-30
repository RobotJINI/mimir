from concurrent import futures
import logging

import grpc
import time
import model.weather_measurement_pb2 as weather_measurement_pb2
import server.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc
from model.database import WeatherDatabase


class WeatherServer(weather_measurement_pb2_grpc.WeatherServer):    
    def __init__(self, port='50051'):
        self._port = port
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        weather_measurement_pb2_grpc.add_WeatherServerServicer_to_server(self.WeatherGrpcServer(), self._server)
        self._server.add_insecure_port('[::]:' + self._port)
        self._running = False
        
    def run(self):
        self._server.start()
        self._running = True
        while self._running:
            time.sleep(.1)
            
    def stop(self):
        self._running = False
        self._server.stop(1)
        
        
    class WeatherGrpcServer(weather_measurement_pb2_grpc.WeatherServer):
        def __init__(self):
            weather_measurement_pb2_grpc.WeatherServer.__init__(self)

        def get_measurements(self, request, context):
            try:
                weather_database = WeatherDatabase()
                query_response = weather_database.get_historical_weather(start_time, end_time)
                measurement_response = self._query_to_measurement_response(query_response)
                return measurement_response
            except Exception as e:
                print(f'Error get_measurements failed!\n{e}')
                return weather_measurement_pb2.MeasurementResponse()
            
        def get_current_weather(self, request, context):
            try:
                end_time = self._get_time_ms()
                start_time = end_time - (request.duration * 1000)
                weather_database = WeatherDatabase()
                
                query_response = weather_database.get_current_weather(start_time, end_time)
                uv_risk_lv = weather_database.get_latest_uv_risk()
                average_wind_dir = weather_database.get_average_wind_dir(start_time, end_time)
                
                current_weather_response = self._query_to_current_weather_response(query_response, uv_risk_lv, average_wind_dir, end_time)
                
                return current_weather_response       
            except Exception as e:
                print(f'Error get_current_weather failed!\n{e}')
                return weather_measurement_pb2.CurrentWeatherResponse()
            
        def _query_to_current_weather_response(self, query_response, uv_risk_lv, average_wind_dir, time):
            query_response = query_response[0]
            return weather_measurement_pb2.CurrentWeatherResponse(
                    time=int(time), 
                    air_temp=str(query_response['air_temp']), 
                    pressure=str(query_response['pressure']), 
                    humidity=str(query_response['humidity']), 
                    ground_temp=str(query_response['ground_temp']), 
                    uv=str(query_response['uv']), 
                    uv_risk_lv=str(uv_risk_lv), 
                    wind_speed=str(query_response['wind_speed']),
                    wind_gust=str(query_response['gust']) ,
                    rainfall=str(query_response['rainfall']), 
                    rain_rate=str(query_response['rain_rate']), 
                    wind_dir=str(average_wind_dir))

        def _query_to_measurement_response(self, query_response):
            measurement_response = weather_measurement_pb2.MeasurementResponse()
            for db_measurement in query_response:
                proto_measurement = weather_measurement_pb2.Measurement(
                                        time=int(db_measurement['time']), 
                                        air_temp=str(db_measurement['air_temp']), 
                                        pressure=str(db_measurement['pressure']), 
                                        humidity=str(db_measurement['humidity']), 
                                        ground_temp=str(db_measurement['ground_temp']), 
                                        uv=str(db_measurement['uv']), 
                                        uv_risk_lv=str(db_measurement['uv_risk_lv']), 
                                        wind_speed=str(db_measurement['wind_speed']), 
                                        rainfall=str(db_measurement['rainfall']), 
                                        rain_rate=str(db_measurement['rain_rate']), 
                                        wind_dir=str(db_measurement['wind_dir'])
                                    )
                measurement_response.measurements.append(proto_measurement)
              
            return measurement_response
        
        def _get_time_ms(self):
            return time.time() * 1000
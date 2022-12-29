from __future__ import print_function

import logging

import grpc
import time
import model.weather_measurement_pb2 as weather_measurement_pb2
import server.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to get measurement ...")
    with grpc.insecure_channel('192.168.1.248:50051') as channel:
        stub = weather_measurement_pb2_grpc.WeatherServerStub(channel)
        current = get_time_ms()
        response = stub.get_measurements(weather_measurement_pb2.MeasurementRequest(start_time=int(current-2000), end_time=int(current)))
    print(f'response:{response.measurements}')
    
def get_time_ms():
    return time.time() * 1000


if __name__ == '__main__':
    logging.basicConfig()
    run()
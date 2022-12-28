from __future__ import print_function

import logging

import grpc
import model.weather_measurement_pb2 as weather_measurement_pb2
import server.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to get measurement ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_measurement_pb2_grpc.WeatherServerStub(channel)
        response = stub.get_measurements(weather_measurement_pb2.MeasurementRequest(start_time=0, end_time=1338))
    print(f'response:{response.measurements}')


if __name__ == '__main__':
    logging.basicConfig()
    run()
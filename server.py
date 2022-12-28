from concurrent import futures
import logging

import grpc
import model.weather_measurement_pb2 as weather_measurement_pb2
import server.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc


class WeatherServer(weather_measurement_pb2_grpc.WeatherServer):

    def get_measurements(self, request, context):
        measurement = weather_measurement_pb2.Measurement(time=1337, air_temp='46.3412', pressure='2456.7342', humidity='11.5241', 
                                                                  ground_temp='34.6451', uv='5.1499', uv_risk_lv='LOW', wind_speed='5.6723', 
                                                                  rainfall='0.2781', rain_rate='0.1507', wind_dir=15)
        measurement_response = weather_measurement_pb2.MeasurementResponse()
        measurement_response.measurements.append(measurement)
        return measurement_response


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_measurement_pb2_grpc.add_WeatherServerServicer_to_server(WeatherServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
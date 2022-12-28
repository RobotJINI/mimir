# mimir

Custom weather station on raspberry pi 3 written in python


Database

create database weather;

use weather;

CREATE TABLE weather_measurement(
id BIGINT NOT NULL AUTO_INCREMENT,
time BIGINT NOT NULL,
air_temp DECIMAL(8,4) NOT NULL,
pressure DECIMAL(8,4) NOT NULL,
humidity DECIMAL(8,4) NOT NULL,
ground_temp DECIMAL(8,4) NOT NULL,
uv DECIMAL(8,4) NOT NULL,
uv_risk_lv VARCHAR(8) NOT NULL,
wind_speed DECIMAL(8,4) NOT NULL,
rainfall DECIMAL(8,4) NOT NULL,
rain_rate DECIMAL(8,4) NOT NULL,
wind_dir INT NOT NULL,
PRIMARY KEY (id)
);

Proto compile:

python3 -m grpc_tools.protoc -I=./protos/ --python_out=./model/ --grpc_python_out=./server/ ./protos/weather_measurement.proto
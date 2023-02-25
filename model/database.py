import MySQLdb, datetime, http.client, json, os
import io
import math


class WeatherDatabase:
    def __init__(self):
        self._db = self.MysqlDatabase()
        self._insert_template = 'INSERT INTO weather_measurement (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, ' + \
                                'rain_rate, wind_dir) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

        self._historical_weather_template = 'SELECT time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir ' + \
                                            'FROM weather_measurement ' + \
                                            'WHERE time BETWEEN %s AND %s;'

        self._current_weather_template = 'SELECT AVG(air_temp) as air_temp, AVG(pressure) as pressure, AVG(humidity) as humidity, ' + \
                                         'AVG(ground_temp) as ground_temp, AVG(uv) as uv, AVG(wind_speed) as wind_speed, MAX(wind_speed) as gust, ' + \
                                         'AVG(rainfall) as rainfall, AVG(rain_rate) as rain_rate ' + \
                                         'FROM weather_measurement ' + \
                                         'WHERE time BETWEEN %s AND %s;'

        self._latest_uv_template = 'SELECT uv_risk_lv FROM weather_measurement LIMIT 1;'

        self._current_wind_dir_template = 'SELECT wind_dir ' + \
                                          'FROM weather_measurement ' + \
                                          'WHERE time BETWEEN %s AND %s AND NOT wind_dir=-1;'

    def insert(self, time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir):
        params = (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir)
        print(self._insert_template % params)
        self._db.execute(self._insert_template, params)

    def get_historical_weather(self, start_time, end_time):
        params = (start_time, end_time)
        return self._db.query(self._historical_weather_template % params)

    def get_current_weather(self, start_time, end_time):
        params = (start_time, end_time)
        return self._db.query(self._current_weather_template % params)

    def get_latest_uv_risk(self):
        query_response = self._db.query(self._latest_uv_template)
        return query_response[0]['uv_risk_lv']

    def get_average_wind_dir(self, start_time, end_time):
        params = (start_time, end_time)
        query_response = self._db.query(self._current_wind_dir_template % params)
        return self._average_wind_dir(query_response)

    def _average_wind_dir(self, query_response):
        sin_sum = 0.0
        cos_sum = 0.0

        flen = float(len(query_response))
        if flen == 0:
            return -1

        for angle_response in query_response:
            angle = angle_response['wind_dir']
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average


    class MysqlDatabase:
        def __init__(self):
            credentials_file = os.path.join(os.path.dirname(__file__), "../config/credentials.mysql")
            f = open(credentials_file, "r")
            credentials = json.load(f)
            f.close()
            for key, value in credentials.items(): #remove whitespace
                credentials[key] = value.strip()

            self._connection = MySQLdb.connect(user=credentials["USERNAME"], password=credentials["PASSWORD"], database=credentials["DATABASE"])

        def execute(self, query, params = []):
            try:
                self._connection.cursor().execute(query, params)
                self._connection.commit()
            except:
                self._connection.rollback()
                raise

        def query(self, query):
            cursor = self._connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query)
            return cursor.fetchall()

        def __del__(self):
            self._connection.close()

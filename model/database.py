import MySQLdb, datetime, http.client, json, os
import io


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
                                         'AVG(rainfall) as rainfall, AVG(rain_rate) as rain_rate, AVG(wind_dir) as wind_dir ' + \
                                         'FROM weather_measurement ' + \
                                         'WHERE time BETWEEN %s AND %s;'
                                         
        self._get_latest_uv_template = 'SELECT uv_risk_lv FROM weather_measurement LIMIT 1;'

    def insert(self, time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir):
        params = (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir)
        print(f'{self._insert_template % params}\n')
        self._db.execute(self._insert_template, params)
        
    def get_historical_weather(self, start_time, end_time):
        params = (start_time, end_time)
        return self._db.query(self._query_template % params)
    
    def get_current_weather(self, start_time, end_time):
        params = (start_time, end_time)
        print(f'{self._current_weather_template % params}\n')
        return self._db.query(self._current_weather_template % params)
    
    def get_latest_uv_risk(self):
        return self._db.query(self._get_latest_uv_template)
    
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
        
import MySQLdb, datetime, http.client, json, os
import io


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
        

class WeatherDatabase:
    def __init__(self):
        self._db = MysqlDatabase()
        self._insert_template = 'INSERT INTO weather_measurement (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, ' + \
                                'rain_rate, wind_dir) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

    def insert(self, time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir):
        params = (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall,rain_rate, wind_dir)
        print(self._insert_template % params)
        self._db.execute(self._insert_template, params)

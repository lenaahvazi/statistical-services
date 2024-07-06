from apscheduler.schedulers.background import BackgroundScheduler
import cherrypy
import requests
import statistics
import config
from helpers import register


class SensorStatsAPI:

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_stats(self, sensor_name, place_id):
        data = self.get_sensor_data(sensor_name, place_id)
        if data:
            stats = self.calculate_statistics(data)
            return stats
        else:
            cherrypy.response.status = 404
            return {"error": "No data found or failed to retrieve data"}

    def get_sensor_data(self, sensor_name, place_id):
        try:
            params = {
                'sensor_name': sensor_name,
                'place_id': place_id
            }

            response = requests.get(url=config.historicalDataIP, params=params)
            response.raise_for_status()
            data = response.json()

            return data
        except requests.exceptions.HTTPError as http_err:
            cherrypy.log(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            cherrypy.log(f"An error occurred: {err}")
            return None

    def extract_values(self, sensor_data):
        values = [entry['value'] for entry in sensor_data]
        return values

    def calculate_statistics(self, raw_data):
        values = self.extract_values(raw_data)

        if not values:
            return {}

        stats = {}
        stats['data'] = raw_data
        stats['mean'] = round(statistics.mean(values), 2)
        stats['median'] = round(statistics.median(values), 2)

        try:
            stats['mode'] = round(statistics.mode(values), 2)
        except statistics.StatisticsError:
            stats['mode'] = None  # No unique mode

        stats['min'] = round(min(values), 2)
        stats['max'] = round(max(values), 2)
        stats['range'] = round(stats['max'] - stats['min'], 2)
        stats['variance'] = round(statistics.variance(values), 2) if len(values) > 1 else None
        stats['standard_deviation'] = round(statistics.stdev(values), 2) if len(values) > 1 else None

        return stats


scheduler = BackgroundScheduler()

if __name__ == "__main__":
    register()

    interval = config.registerInterval
    scheduler.add_job(register, 'interval', seconds=interval)
    scheduler.start()

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 7010,
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    })

    try:
        cherrypy.quickstart(SensorStatsAPI(), '/api/v1')
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

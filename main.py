#from flask import Flask, request
from bottle import Bottle, run, request

from threading import Lock
import copy
from apscheduler.schedulers.background import BackgroundScheduler
from influxdb import InfluxDBClient
from datetime import datetime as dt
import logging
logfl = logging.getLogger('werkzeug')
logfl.setLevel(logging.ERROR)


#app = Flask(__name__)
app=Bottle()

# Influx access
host = '172.17.0.1'
port = 8086
USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'
DB = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
DB.create_database(DBNAME)

points = []
points_lock = Lock()

def request2point(data):
    """ JSON in, influx format out """
    now = dt.now()
    device_id = data['dev_id']

    key0 = 'Counter0'
    key1 = 'Counter1'
    value_0 = data[key0]
    value_1 = data[key1]
    point = {
        "measurement": '{}'.format(device_id),
        "time": now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "in_1": value_0,
            "in_2": value_1
        }
    }

    return point

@app.route('/zupa', methods=['POST', 'GET'])
def zupa():
    print(request.headers)
    print(request.json)
    point = request2point(request.json)
    with points_lock:
        points.append(point)
    # print(points)
    return 'dupa'

@app.route('/dupa/<dev_id>/<value>', methods=['POST'])
def dupa(dev_id, value):
    print(request.view_args['dev_id'])
    print(request.view_args['value'])
    print(request.json)
    print(request.headers)
    return 'dupa'


def tick():
    global points
    with points_lock:
        #temp_points=copy.deepcopy(points)
        temp_points=list(points)
        points=[]
    print(temp_points)
    DB.write_points(temp_points)

    

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=5)
    scheduler.start()
    #app.run(host='0.0.0.0', port=81, debug=True)
    run(app, host='0.0.0.0', port=81, debug=True)


from flask import Flask, request
from influxdb import InfluxDBClient
from datetime import datetime as dt

app = Flask(__name__)

# Influx access
host = 'localhost'
port = 8086
USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'
DB = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
DB.create_database(DBNAME)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def request2points(data):
    """ JSON in, influx format out """
    now = dt.now()
    device_id = data['dev_id']

    key0 = 'Counter0'
    key1 = 'Counter1'
    value_0 = data[key0]
    value_1 = data[key1]
    points = [{
        "measurement": '{}'.format(device_id),
        "time": now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "value_0": value_0,
            "value_1": value_1
        }
    }]

    return points

@app.route('/zupa', methods=['POST', 'GET'])
def zupa():
    # print(request.headers)
    # print(request.json)
    points = request2points(request.json)
    print(points)
    DB.write_points(points)
    return 'dupa'

@app.route('/dupa/<dev_id>/<value>', methods=['POST'])
def dupa(dev_id, value):
    print(request.view_args['dev_id'])
    print(request.view_args['value'])
    print(request.json)
    print(request.headers)
    return 'dupa'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432, debug=True)

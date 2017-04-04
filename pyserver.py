import math, json, socket
import os, errno
import peewee
from peewee import *

from flask import Flask, request
app = Flask(__name__)


db = MySQLDatabase('l2d_points', user='l2d', passwd='cubin123')

class Points(peewee.Model):
    lat = peewee.FloatField()
    lng = peewee.FloatField()
    country_code = peewee.CharField()

    class Meta:
        database = db

# point = Points(lat='10.6', lng='107.1', country_code='AT')
# point.save()

# for p in Points.filter(country_code='AT'):
#     print(p.lat)


# =================================================================================
@app.route('/')
def index():
    return ''

# =================================================================================
@app.route('/create', methods=['POST'])
def create():
    data = request.json

    country_code = data['country_code']
    coordinates = data['coordinates']
    lng = coordinates[0]
    lat = coordinates[1]

    if country_code is None or lat is None or lng is None:
        dict = {
            "error_code": 2,
            "message": "Invalid JSON request"
        }
        return json.dumps(dict)

    existing_points = Points.filter(country_code=country_code)

    if len(existing_points) > 0:
        dict = {
                "error_code": 1,
                "message": "Existed country code"
        }
        return json.dumps(dict)
    else:
        point = Points(lat=lat, lng=lng, country_code=country_code)
        point.save()
        dict = {
            "error_code": 0,
            "message": "Create successfully"
        }
        return json.dumps(dict)
# =================================================================================
@app.route('/update', methods=['POST'])
def update():
    data = request.json
    country_code = data['country_code']
    coordinates = data['coordinates']
    lng = coordinates[0]
    lat = coordinates[1]

    if country_code is None or lat is None or lng is None:
        dict = {
            "error_code": 2,
            "message": "Invalid JSON request"
        }
        return json.dumps(dict)

    for p in Points.filter(country_code=country_code):
        if p.country_code == country_code:
            p.lat = lat
            p.lng = lng
            p.country_code = country_code
            p.save()
            dict = {
                "error_code": 0,
                "message": "Update successfully"
            }
            return json.dumps(dict)
    dict = {
        "error_code": 3,
        "message": "Not found requesting point"
    }
    return json.dumps(dict)

# =================================================================================
@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    country_code = data['country_code']

    for p in Points.filter(country_code=country_code):
        if p.country_code == country_code:
            p.delete_instance()
            dict = {
                "error_code": 0,
                "message": "Delete successfully"
            }
            return json.dumps(dict)
# =================================================================================
@app.route('/points', methods=['GET'])
def points():
    dict = {}
    pointArray = []
    for p in Points.select():
        point = {
            "type": "Point",
            "coordinates": [p.lng, p.lat],
            "country_code": p.country_code
        }
        pointArray.append(point)

    dict['result'] = pointArray
    return json.dumps(dict)

app.run(host='localhost', port=5000)
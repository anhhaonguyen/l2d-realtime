import json
import peewee
from peewee import *

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return ''
# ======================================


@app.route('/create', methods=['POST'])
def create():
    data = request.json

    country_code = data['country_code']
    coordinates = data['coordinates']
    lng = coordinates[0]
    lat = coordinates[1]

    if country_code is None or lat is None or lng is None:
        info = {
            "error_code": 2,
            "message": "Invalid JSON request"
        }
        return json.dumps(info)

    db = MySQLDatabase('l2d_points', user='l2d', passwd='cubin123')

    class Points(peewee.Model):
        lat = peewee.FloatField()
        lng = peewee.FloatField()
        country_code = peewee.CharField()

        class Meta:
            database = db

    existing_points = Points.filter(country_code=country_code)

    if len(existing_points) > 0:
        info = {
            "error_code": 1,
            "message": "Existed country code"
        }
        db.close()
        return json.dumps(info)
    else:
        point = Points(lat=lat, lng=lng, country_code=country_code)
        point.save()
        info = {
            "error_code": 0,
            "message": "Create successfully"
        }
        db.close()
        return json.dumps(info)
# ======================================


@app.route('/update', methods=['POST'])
def update():
    data = request.json
    country_code = data['country_code']
    coordinates = data['coordinates']
    lng = coordinates[0]
    lat = coordinates[1]

    if country_code is None or lat is None or lng is None:
        info = {
            "error_code": 2,
            "message": "Invalid JSON request"
        }
        return json.dumps(info)

    db = MySQLDatabase('l2d_points', user='l2d', passwd='cubin123')

    class Points(peewee.Model):
        lat = peewee.FloatField()
        lng = peewee.FloatField()
        country_code = peewee.CharField()

        class Meta:
            database = db

    for p in Points.filter(country_code=country_code):
        if p.country_code == country_code:
            p.lat = lat
            p.lng = lng
            p.country_code = country_code
            p.save()
            info = {
                "error_code": 0,
                "message": "Update successfully"
            }
            db.close()
            return json.dumps(info)
    info = {
        "error_code": 3,
        "message": "Not found requesting point"
    }
    db.close()
    return json.dumps(info)
# ======================================


@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    country_code = data['country_code']

    db = MySQLDatabase('l2d_points', user='l2d', passwd='cubin123')

    class Points(peewee.Model):
        lat = peewee.FloatField()
        lng = peewee.FloatField()
        country_code = peewee.CharField()

        class Meta:
            database = db

    for p in Points.filter(country_code=country_code):
        if p.country_code == country_code:
            p.delete_instance()
            info = {
                "error_code": 0,
                "message": "Delete successfully"
            }
            db.close()
            return json.dumps(info)
# ======================================


@app.route('/points', methods=['GET'])
def points():
    info = {}
    point_array = []
    db = MySQLDatabase('l2d_points', user='l2d', passwd='cubin123')

    class Points(peewee.Model):
        lat = peewee.FloatField()
        lng = peewee.FloatField()
        country_code = peewee.CharField()

        class Meta:
            database = db

    for p in Points.select():
        point = {
            "type": "Point",
            "coordinates": [p.lng, p.lat],
            "country_code": p.country_code
        }
        point_array.append(point)

    info['result'] = point_array
    db.close()
    return json.dumps(info)
# ======================================


app.run(host='0.0.0.0', port=5000)

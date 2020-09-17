from database.postsqldb.db import db
from geoalchemy2.types import Geometry
from flask_restful import fields
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'model': fields.String,
    'doors': fields.Integer
}
class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"

neighborhood_fields = {
    'gid': fields.Integer,
    'boroname': fields.String,
    'name': fields.String
}

neighborhood_area_fields = {
    'name': fields.String
    #'bufferarea':fields.Float
}
class NeighborhoodModel(db.Model):
    __bind_key__ = 'nyc'
    __tablename__ = 'nyc_neighborhoods'
    gid = db.Column(db.Integer, primary_key=True)
    boroname = db.Column(db.String(43))
    name = db.Column(db.String(64))
    geom = db.Column(Geometry(geometry_type='POINT', srid=26918))


class Geometries3Model(db.Model):
    __bind_key__ = 'nyc'
    __tablename__ = 'geometries3'
    name = db.Column(db.String(64),primary_key=True)
    geom = db.Column(Geometry(geometry_type='LINESTRINGM', srid=4326))
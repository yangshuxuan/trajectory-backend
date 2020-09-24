from database.postsqldb.db import db
from datetime import datetime
from geoalchemy2.types import Geometry
from flask_restful import fields
from geoalchemy2.elements import WKTElement

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

class LastappearedModel(db.Model):
    __bind_key__ = 'nyc'
    __tablename__ = 'lastappeared'
    object_id = db.Column(db.String(50), primary_key=True)
    lastmodified_time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    gps_point = db.Column(Geometry(geometry_type='POINT', srid=4326))
    def __init__(self,**kwargs):
        if "lat" in kwargs.keys() and "long" in kwargs.keys() and "gps_point" not in kwargs.keys():
            kwargs["gps_point"] = 'SRID=4326;POINT({} {})'.format(kwargs["long"],kwargs["lat"])
            del kwargs["lat"]
            del kwargs["long"]
        if "lastmodified_time" in kwargs.keys() and type(kwargs["lastmodified_time"]) is str:
            lastmodified_time_str = kwargs["lastmodified_time"]
            kwargs["lastmodified_time"] = datetime.strptime(lastmodified_time_str, "%Y-%m-%d %H:%M:%S")

        super(LastappearedModel, self).__init__(**kwargs)
    def update(self,body):
        if "lat" in body.keys() and "long" in body.keys():
            self.gps_point = 'SRID=4326;POINT({} {})'.format(body["long"],body["lat"])
 
        if "lastmodified_time" in body.keys() and type(body["lastmodified_time"]) is str:
            lastmodified_time_str = body["lastmodified_time"]
            self.lastmodified_time = datetime.strptime(lastmodified_time_str, "%Y-%m-%d %H:%M:%S")

    def lat(self):
        return db.session.scalar(self.gps_point.ST_Y())
    def long(self):
        return db.session.scalar(self.gps_point.ST_X())
    def dictRepr(self):
        return {"object_id":self.object_id,"lastmodified_time":self.lastmodified_time.strftime("%Y-%m-%d %H:%M:%S"),"long":self.long(),"lat":self.lat()}


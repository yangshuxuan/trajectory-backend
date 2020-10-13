from database.postsqldb.db import db
from datetime import datetime
from geoalchemy2.types import Geometry
from flask_restful import fields
from geoalchemy2.elements import WKTElement
from statsmodels.tsa.statespace.varmax import VARMAX
from random import random
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

    exception_type = db.relationship('ExceptionTypeModel',uselist=False,  lazy=True)
    machine_type = db.relationship('MachineTypeModel',uselist=False,  lazy=True)
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
        info = {"object_id":self.object_id,"lastmodified_time":self.lastmodified_time.strftime("%Y-%m-%d %H:%M:%S"),"long":self.long(),"lat":self.lat()}
        if self.exception_type is not None:
            info["exception_type"] = self.exception_type.exceptiontype
        if self.machine_type is not None:
            info["machine_type"] = self.machine_type.machinetype

        return info 

class ObjectTrajactoryModel(db.Model):
    __tablename__ = 'objecttrajactory'
    object_id = db.Column(db.String(50),primary_key=True)
    gps_line = db.Column(Geometry(geometry_type='LINESTRINGM', srid=4326))
    #p = ObjectTrajactoryModel(object_id='Ortab', gps_line='SRID=4326;LINESTRINGM(0 0 20, 1 1 21, 2 1 22, 2 2 23)')
    def __init__(self,**kwargs):
        if "gps_points" in kwargs.keys() and "gps_line" not in kwargs.keys():
            #timestamp = datetime.timestamp(now)
            kwargs["gps_line"] = 'SRID=4326;LINESTRINGM({})'.format(",".join(["{} {} {}".format(
                p["long"],p["lat"],datetime.timestamp(datetime.strptime(p["occurtime"], "%Y-%m-%d %H:%M:%S"))
                ) for p in kwargs["gps_points"]]))
            del kwargs["gps_points"]


        super(ObjectTrajactoryModel, self).__init__(**kwargs)
    def gps_points(self):
        gps_points = []
        for i in range(1,db.session.scalar(self.gps_line.ST_NPoints()) + 1):
            gps_point = {}
            gps_point["occurtime"] =  datetime.fromtimestamp(db.session.scalar(self.gps_line.ST_PointN(i).ST_M())).strftime("%Y-%m-%d %H:%M:%S")
            gps_point["long"] =  db.session.scalar(self.gps_line.ST_PointN(i).ST_X())
            gps_point["lat"] =  db.session.scalar(self.gps_line.ST_PointN(i).ST_Y())
            gps_points.append(gps_point)
        return gps_points
    def precictTrajectory(self):
        predict_num = 5
        gps_points = self.gps_points()
        # data = [[p["long"],p["lat"]] for p in gps_points]
        data = list()
        for i in range(100):
            v1 = random()
            v2 = v1 + random()
            row = [v1, v2]
            data.append(row)
        model = VARMAX(data, order=(1, 1))
        model_fit = model.fit(disp=False)

        yhat = model_fit.forecast(predict_num)
        return {"object_id":self.object_id,"gps_points": [{"long":p[0],"lat":p[1]} for p in yhat]}
        

    def update(self,body):
        
        for p in body["gps_points"]:
            toAddPoint ='POINTM({} {} {})'.format(p["long"],p["lat"],datetime.timestamp(datetime.strptime(p["occurtime"], "%Y-%m-%d %H:%M:%S")))
            self.gps_line = db.session.scalar(self.gps_line.ST_AddPoint(toAddPoint))
        
    def dictRepr(self):
        return {"object_id":self.object_id,"gps_points":self.gps_points()}




class AirLineModel(db.Model):
    __tablename__ = 'airline'

    id = db.Column(db.Integer, primary_key=True)
    airlinecode = db.Column(db.String(80), unique=True, nullable=False) #air line number
    airlinegps = db.Column(Geometry(geometry_type='LINESTRING', srid=4326),nullable=False)


class ObjectUseAirlineModel(db.Model):
    __tablename__ = 'object_use_airline'
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.String(50),nullable=False)
    flight_task_number = db.Column(db.String(50),nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    airline_id = db.Column(db.Integer, db.ForeignKey('airline.id'),
        nullable=False)


class MachineTypeModel(db.Model):
    __tablename__ = 'machinetype'

    object_id = db.Column(db.String(50),db.ForeignKey('lastappeared.object_id'),primary_key=True)
    machinetype = db.Column(db.String())


class ExceptionTypeModel(db.Model):
    __tablename__ = 'exceptiontype'
    object_id = db.Column(db.String(50),db.ForeignKey('lastappeared.object_id'),primary_key=True)
    exceptiontype = db.Column(db.String())

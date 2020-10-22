from database.postsqldb.db import db
from datetime import datetime
from geoalchemy2.types import Geometry
from flask_restful import fields
from geoalchemy2.elements import WKTElement
from statsmodels.tsa.statespace.varmax import VARMAX
from random import random
from sqlalchemy.ext.declarative import declared_attr
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
    __tablename__ = 'lastappeared'
    def defaultDate():
        return datetime.now().date()
    def defaultTime():
        return datetime.now().time()
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.String(50), nullable=False)
    lastmodified_date = db.Column(db.Date, nullable=False,default=defaultDate)
    lastmodified_time = db.Column(db.Time, nullable=False,default=defaultTime)
    gps_point = db.Column(Geometry(geometry_type='POINTM', srid=4326),nullable=False)
    exception_type = db.relationship('ExceptionTypeModel',uselist=False, backref='lastappeared', lazy=True,cascade="all, delete",passive_deletes=True)
    machine_type = db.relationship('MachineTypeModel',uselist=False,  backref='lastappeared',lazy=True,cascade="all, delete",passive_deletes=True)
    object_trajactory = db.relationship('ObjectTrajactoryModel',uselist=False,  backref='lastappeared',lazy=True,cascade="all, delete",passive_deletes=True)
    __table_args__ = (db.UniqueConstraint('object_id', 'lastmodified_date'), )
    def __init__(self,**kwargs):
        if "lastmodified_time" in kwargs.keys() and type(kwargs["lastmodified_time"]) is str:
            lastmodified_date_time_str = kwargs["lastmodified_time"]
            kwargs["lastmodified_date_time"] = datetime.strptime(lastmodified_date_time_str, "%Y-%m-%d %H:%M:%S")
        else:
            kwargs["lastmodified_date_time"] = datetime.now()
        if "lastmodified_date" not in kwargs.keys() or type(kwargs["lastmodified_date"]) is str:
            kwargs["lastmodified_date"] = kwargs["lastmodified_date_time"].date()
        if "lastmodified_time" not in kwargs.keys() or type(kwargs["lastmodified_time"]) is str:
            kwargs["lastmodified_time"] = kwargs["lastmodified_date_time"].time()
        if "lat" in kwargs.keys() and "long" in kwargs.keys() and "gps_point" not in kwargs.keys():
            kwargs["gps_point"] = 'SRID=4326;POINTM({} {} {})'.format(kwargs["long"],kwargs["lat"],datetime.timestamp(kwargs["lastmodified_date_time"]))
            del kwargs["lat"]
            del kwargs["long"]
        del kwargs["lastmodified_date_time"]
        

        super(LastappearedModel, self).__init__(**kwargs)
    def update(self,body):
        if "lastmodified_time" in body.keys() and type(body["lastmodified_time"]) is str:
            lastmodified_date_time_str = body["lastmodified_time"]
            lastmodified_date_time = datetime.strptime(lastmodified_date_time_str, "%Y-%m-%d %H:%M:%S")
        else:
            lastmodified_date_time = datetime.now()
        self.lastmodified_date = lastmodified_date_time.date()
        self.lastmodified_time = lastmodified_date_time.time()
        if "lat" in body.keys() and "long" in body.keys():
            self.gps_point = 'SRID=4326;POINTM({} {} {})'.format(body["long"],body["lat"],datetime.timestamp(lastmodified_date_time))
        
 
        

    def lat(self):
        return db.session.scalar(self.gps_point.ST_Y())
    def long(self):
        return db.session.scalar(self.gps_point.ST_X())
    def M(self):
        return db.session.scalar(self.gps_point.ST_M())
    def dictRepr(self):
        info = {"id":self.id,"object_id":self.object_id,
        "lastmodified_date":self.lastmodified_date.strftime("%Y-%m-%d"),
        "lastmodified_time":self.lastmodified_time.strftime("%H:%M:%S"),"long":self.long(),"lat":self.lat(),"M":self.M()}
        if self.exception_type is not None:
            info["exception_type"] = self.exception_type.exceptiontype
        if self.machine_type is not None:
            info["machine_type"] = self.machine_type.machinetype

        return info 


class TrajectoryMixin:
    @declared_attr
    def lastappeared_id(cls):
        return db.Column(db.Integer,db.ForeignKey('lastappeared.id',ondelete="CASCADE"),primary_key=True)
    gps_line = db.Column(Geometry(geometry_type='LINESTRINGM', srid=4326))
    def gps_points(self):
        gps_points = []
        for i in range(1,db.session.scalar(self.gps_line.ST_NPoints()) + 1):
            gps_point = {}
            gps_point["occurtime"] =  datetime.fromtimestamp(db.session.scalar(self.gps_line.ST_PointN(i).ST_M())).strftime("%Y-%m-%d %H:%M:%S")
            gps_point["long"] =  db.session.scalar(self.gps_line.ST_PointN(i).ST_X())
            gps_point["lat"] =  db.session.scalar(self.gps_line.ST_PointN(i).ST_Y())
            gps_points.append(gps_point)
        return gps_points
    def dictRepr(self,**kwargs):
        d = {"id":self.lastappeared.id,"object_id":self.lastappeared.object_id,
        "lastmodified_date":self.lastappeared.lastmodified_date.strftime("%Y-%m-%d"),"gps_points":self.gps_points()}
        
        if "similar" in kwargs:
            d["similar"] = kwargs["similar"]
        return d
class ObjectTrajactoryModel(TrajectoryMixin,db.Model):
    __tablename__ = 'objecttrajactory'
        
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
        
        return {"object_id":self.lastappeared.object_id,"gps_points": [{"long":p[0],"lat":p[1]} for p in yhat]}
        
        
    




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

    lastappeared_id = db.Column(db.Integer,db.ForeignKey('lastappeared.id',ondelete="CASCADE"),primary_key=True)
    machinetype = db.Column(db.String())
    def dictRepr(self):
        return {"lastappeared_id":self.lastappeared_id,"machinetype":self.machinetype}


class ExceptionTypeModel(db.Model):
    __tablename__ = 'exceptiontype'
    lastappeared_id = db.Column(db.Integer,db.ForeignKey('lastappeared.id',ondelete="CASCADE"),primary_key=True)
    exceptiontype = db.Column(db.String())
    def dictRepr(self):
        return {"lastappeared_id":self.lastappeared_id,"exceptiontype":self.exceptiontype}

from flask import request
from database.postsqldb.models import LastappearedModel,MachineTypeModel,ExceptionTypeModel
from datetime import datetime
from database.postsqldb.db import db
from sqlalchemy.sql import select, func

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields
from flask_restful import reqparse

class LastappearedApiByObjectID(Resource):
  def put(self, object_id):
    body = request.get_json()
    body["object_id"] = object_id
    if "lastmodified_time" in body.keys() and type(body["lastmodified_time"]) is str:
      lastmodified_date_time_str = body["lastmodified_time"]
      lastmodified_date_time = datetime.strptime(lastmodified_date_time_str, "%Y-%m-%d %H:%M:%S")
    else:
      lastmodified_date_time = datetime.now()

    lastappearedModel = LastappearedModel.query.filter_by(lastmodified_date = lastmodified_date_time.date(),object_id = object_id).first()
    body["lastmodified_time"] = lastmodified_date_time.strftime("%Y-%m-%d %H:%M:%S")
    
    if lastappearedModel is None:
      
      lastappearedModel = LastappearedModel(**body)
      db.session.add(lastappearedModel)
    else:
      lastappearedModel.update(body)

    db.session.commit()
    return {'id': lastappearedModel.id,'object_id': lastappearedModel.object_id}
class LastappearedApi(Resource):
  def get(self,id):
    lastappearedModel = LastappearedModel.query.get(id)
    return lastappearedModel.dictRepr(),200
  def delete(self, id):
        lastappearedModel = LastappearedModel.query.get(id)
        if lastappearedModel is not None:
          db.session.delete(lastappearedModel)
          db.session.commit()
        return {'id': id}

class LastappearedsApi(Resource):
  
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('machinetype')
    parser.add_argument('exceptiontype')
    args = parser.parse_args()

    machinetype = args['machinetype']

    exceptiontype = args['exceptiontype']

    if machinetype is not None:
      rows = LastappearedModel.query.join(MachineTypeModel, LastappearedModel.object_id==MachineTypeModel.object_id).filter(MachineTypeModel.machinetype.in_ (machinetype.split(",")) ).all()
    elif exceptiontype is not None:
      rows = LastappearedModel.query.join(ExceptionTypeModel, LastappearedModel.object_id==ExceptionTypeModel.object_id).filter(ExceptionTypeModel.exceptiontype.in_ (exceptiontype.split(",")) ).all()
    else :
      rows = LastappearedModel.query.all()

    return  [row.dictRepr() for row in rows]
  
  def post(self):
    body = request.get_json()
    lastappearedPoint = LastappearedModel(**body)
    db.session.add(lastappearedPoint)
    db.session.commit()
    return {'id': lastappearedPoint.id,'object_id': lastappearedPoint.object_id}, 200
  def delete(self):
    LastappearedModel.query.delete()
    db.session.commit()
    return "succeed to delete", 200
  

class LastappearedsFilterApi(Resource):
  
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('machinetype')
    parser.add_argument('exceptiontype')
    parser.add_argument('lastmodified_time_range')
    parser.add_argument('lastoccur_region')
    args = parser.parse_args()

    machinetype = args['machinetype']

    exceptiontype = args['exceptiontype']

    lastmodified_time_range = args['lastmodified_time_range']

    lastoccur_region = args['lastoccur_region']
    filters = LastappearedModel.query



    if machinetype is not None:
      
      filters = LastappearedModel.query.filter(LastappearedModel.machine_type.has(MachineTypeModel.machinetype.in_ (machinetype.split(","))))
      
    if exceptiontype is not None:
      filters = filters.filter(LastappearedModel.exception_type.has(ExceptionTypeModel.exceptiontype.in_(exceptiontype.split(","))))
      
    if lastmodified_time_range is not None:
      [start,end] = lastmodified_time_range.split(",")
      if start:
        filters = filters.filter(LastappearedModel.lastmodified_time >= datetime.strptime(start, "%Y-%m-%d %H:%M:%S"))
      if end:
        filters = filters.filter(LastappearedModel.lastmodified_time <= datetime.strptime(end, "%Y-%m-%d %H:%M:%S"))
    
    if lastoccur_region is  not None:
      filters = filters.filter(func.ST_Within(LastappearedModel.gps_point,'SRID=4326;POLYGON(({}))'.format(lastoccur_region)))


    return  [row.dictRepr() for row in filters.all()]









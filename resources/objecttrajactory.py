from flask import request
from database.postsqldb.models import ObjectTrajactoryModel
from datetime import datetime
from database.postsqldb.db import db
from sqlalchemy.sql import select, func
from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields
from flask_restful import reqparse
from sqlalchemy import desc,asc

class ObjectTrajactoryApi(Resource):
  def put(self, id):
    body = request.get_json()

    objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
    if objectTrajactory is None:
      body["object_id"] = id
      if len(body["gps_points"]) == 1:
          body["gps_points"] *= 2
      objectTrajactory = ObjectTrajactoryModel(**body)
      db.session.add(objectTrajactory)
    else:
      objectTrajactory.update(body)

    db.session.commit()
    return {'object_id': objectTrajactory.object_id}

  def get(self,id):
    objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
    return objectTrajactory.dictRepr(),200
  def delete(self, id):
      objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
      if objectTrajactory is not None:
        db.session.delete(objectTrajactory)
        db.session.commit()
      return {'object_id':id}

class ObjectTrajactoryPredictorApi(Resource):
  

  def get(self,id):
    objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
     
    return {"currenttrajectory":objectTrajactory.dictRepr(),"futruetrajectorys":objectTrajactory.precictTrajectory()},200

class ObjectTrajactorysApi(Resource):
  
  def get(self):
    return  [row.dictRepr() for row in ObjectTrajactoryModel.query.all()]

  def post(self):
    body = request.get_json()
    objectTrajactory = ObjectTrajactoryModel(**body)
    db.session.add(objectTrajactory)
    db.session.commit()
    return {'object_id': objectTrajactory.object_id}, 200
  def delete(self):
    ObjectTrajactoryModel.query.delete()
    db.session.commit()
    return "succeed to delete", 200

class SimilarObjectTrajactorysApi(Resource):
  from sqlalchemy import desc,asc
  
  def get(self,id):
    parser = reqparse.RequestParser()

    parser.add_argument('similar_num',type=int)

    args = parser.parse_args()
    similar_num = 10 if args['similar_num'] is None else args['similar_num']
    objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
    rows = ObjectTrajactoryModel.query.filter(ObjectTrajactoryModel.object_id!=id).with_entities(ObjectTrajactoryModel,func.ST_HausdorffDistance(ObjectTrajactoryModel.gps_line,func.ST_AsEWKT(objectTrajactory.gps_line)).label('similar')).order_by(asc('similar')).limit(similar_num).all()
    return  [o.dictRepr(similar=1.0/s) for o,s in rows]
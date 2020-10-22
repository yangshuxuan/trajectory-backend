from flask import request
from database.postsqldb.models import ObjectTrajactoryModel
from datetime import datetime, timedelta
from database.postsqldb.db import db
from sqlalchemy.sql import select, func
from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields
from flask_restful import reqparse
from sqlalchemy import desc,asc

class ObjectTrajactoryApi(Resource):
  def get(self,id):
    objectTrajactory = ObjectTrajactoryModel.query.get(id)
    return objectTrajactory.dictRepr(),200


class ObjectTrajactoryPredictorApi(Resource):
  

  def get(self,id):
    objectTrajactory = ObjectTrajactoryModel.query.get(id)
    return {"currenttrajectory":objectTrajactory.dictRepr(),"futruetrajectorys":objectTrajactory.precictTrajectory()},200

class ObjectTrajactorysApi(Resource):
  
  def get(self):
    return  [row.dictRepr() for row in ObjectTrajactoryModel.query.all()]



class SimilarObjectTrajactorysApi(Resource):
  from sqlalchemy import desc,asc

  def get(self,id):
    parser = reqparse.RequestParser()

    parser.add_argument('similar_num',type=int)

    args = parser.parse_args()
    similar_num = 10 if args['similar_num'] is None else args['similar_num']
    objectTrajactory = ObjectTrajactoryModel.query.get(id)
    rows = ObjectTrajactoryModel.query.filter(ObjectTrajactoryModel.lastappeared_id!=id).with_entities(ObjectTrajactoryModel,func.ST_HausdorffDistance(ObjectTrajactoryModel.gps_line,func.ST_AsEWKT(objectTrajactory.gps_line)).label('similar')).order_by(asc('similar')).limit(similar_num).all()
    return  [o.dictRepr(similar=1.0/(s+1)) for o,s in rows]


class ObjectTrajectoryLastNminutesApi(Resource):
  def get(self, minutes):
    t = datetime(2020, 10, 16, 16, 20, 0)
    # t = datetime.now()
    requiredTime = (t - timedelta(minutes=minutes))
    query = ObjectTrajactoryModel.query.filter(
      ObjectTrajactoryModel.gps_line.ST_EndPoint().ST_M() >= requiredTime.timestamp()).all()
    return [row.dictRepr() for row in query]

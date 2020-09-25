from flask import request
from database.postsqldb.models import ObjectTrajactoryModel
from datetime import datetime
from database.postsqldb.db import db

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields


class ObjectTrajactoryApi(Resource):
  def put(self, id):
    body = request.get_json()

    objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
    if objectTrajactory is None:
      body["object_id"] = id
      if len(body["gps_line"]) is 1:
          body["gps_line"] *= 2
      objectTrajactory = ObjectTrajactoryModel(**body)
      db.session.add(objectTrajactory)
    else:
      objectTrajactory.update(body)

    db.session.commit()
    return {'object_id': objectTrajactory.object_id}

  def get(self,id):
    objectTrajactory = ObjectTrajactoryModel.query.filter_by(object_id=id).first()
    return objectTrajactory.dictRepr(),200



class ObjectTrajactorysApi(Resource):
  
  def get(self):
    return  [row.dictRepr() for row in ObjectTrajactoryModel.query.all()]

  def post(self):
    body = request.get_json()
    objectTrajactory = ObjectTrajactoryModel(**body)
    db.session.add(objectTrajactory)
    db.session.commit()
    return {'object_id': objectTrajactory.object_id}, 200

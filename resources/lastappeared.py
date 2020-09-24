from flask import request
from database.postsqldb.models import LastappearedModel
from datetime import datetime
from database.postsqldb.db import db

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields


class LastappearedModelApi(Resource):
  def put(self, id):
    body = request.get_json()

    lastappearedModel = LastappearedModel.query.filter_by(object_id=id).first()
    if lastappearedModel is None:
      body["object_id"] = id
      lastappearedModel = LastappearedModel(**body)
      db.session.add(lastappearedModel)
    else:
      lastappearedModel.update(body)

    db.session.commit()
    return {'object_id': lastappearedModel.object_id}

  def get(self,id):
    lastappearedModel = LastappearedModel.query.filter_by(object_id=id).first()
    return lastappearedModel.dictRepr(),200



class LastappearedsModelApi(Resource):
  
  def get(self):
    return  [row.dictRepr() for row in LastappearedModel.query.all()]

  def post(self):
    body = request.get_json()
    lastappearedPoint = LastappearedModel(**body)
    db.session.add(lastappearedPoint)
    return {'object_id': lastappearedPoint.object_id}, 200






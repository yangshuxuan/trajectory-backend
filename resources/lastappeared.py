from flask import request
from database.postsqldb.models import LastappearedModel,MachineTypeModel
from datetime import datetime
from database.postsqldb.db import db

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields
from flask_restful import reqparse

class LastappearedApi(Resource):
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



class LastappearedsApi(Resource):
  
  def get(self):
    parser = reqparse.RequestParser()

    parser.add_argument('machinetype')
    args = parser.parse_args()
    print(args['machinetype'])
    machinetype = args['machinetype']
    if machinetype is not None:
      rows = LastappearedModel.query.join(MachineTypeModel, LastappearedModel.object_id==MachineTypeModel.object_id).filter(MachineTypeModel.machinetype.in_ (machinetype.split(",")) ).all()
    else:
      rows = LastappearedModel.query.all()




    return  [row.dictRepr() for row in rows]

  def post(self):
    body = request.get_json()
    lastappearedPoint = LastappearedModel(**body)
    db.session.add(lastappearedPoint)
    db.session.commit()
    return {'object_id': lastappearedPoint.object_id}, 200






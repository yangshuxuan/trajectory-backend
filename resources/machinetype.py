from flask import request
from database.postsqldb.models import LastappearedModel,MachineTypeModel,ExceptionTypeModel
from datetime import datetime
from database.postsqldb.db import db
from sqlalchemy.sql import select, func

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields
from flask_restful import reqparse

# class MachinetypeApi(Resource):
#   def put(self, id):
#     body = request.get_json()

#     lastappearedModel = LastappearedModel.query.filter_by(object_id=id).first()
#     if lastappearedModel is None:
#       body["object_id"] = id
#       lastappearedModel = LastappearedModel(**body)
#       db.session.add(lastappearedModel)
#     else:
#       lastappearedModel.update(body)

#     db.session.commit()
#     return {'object_id': lastappearedModel.object_id}

#   def get(self,id):
#     lastappearedModel = LastappearedModel.query.filter_by(object_id=id).first()
#     return lastappearedModel.dictRepr(),200
#   def delete(self, id):
#         lastappearedModel = LastappearedModel.query.filter_by(object_id=id).first()
#         if lastappearedModel is not None:
#           db.session.delete(lastappearedModel)
#           db.session.commit()
#         return {'object_id': id}

class MachinetypesApi(Resource):
  def get(self):
    return [row.dictRepr() for row in MachineTypeModel.query.all()]


  def post(self):
    body = request.get_json()
    machinetype = MachineTypeModel(**body)
    db.session.add(machinetype)
    db.session.commit()
    return machinetype.dictRepr(), 200
  def delete(self):
    MachineTypeModel.query.delete()
    db.session.commit()
    return "succeed to delete", 200
class MachinetypeStatisticsApi(Resource):
  def get(self):
    rows = MachineTypeModel.query.with_entities(MachineTypeModel.machinetype,func.count(MachineTypeModel.machinetype)).group_by(MachineTypeModel.machinetype).all()
    return [{"machinetype":machinetype,"count":count} for machinetype,count in rows]
    #return dict(rows)

 
  











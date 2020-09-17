from flask import request
from database.postsqldb.models import CarsModel

from database.postsqldb.db import db

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import resource_fields


class CarsApi(Resource):
  @marshal_with(resource_fields)
  def get(self):
    return  CarsModel.query.all()


  def post(self):

    body = request.get_json()
    new_car = CarsModel(**body)
    db.session.add(new_car)
    db.session.commit()
    id = new_car.id
    return {'id': str(id)}, 200

class CarApi(Resource):
  @marshal_with(resource_fields)
  def get(self,id):
    return CarsModel.query.filter_by(id=id).all()


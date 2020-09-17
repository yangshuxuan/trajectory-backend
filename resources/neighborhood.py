from flask import request
from database.postsqldb.models import NeighborhoodModel

from database.postsqldb.db import db

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields


class NeighborhoodsApi(Resource):
  @marshal_with(neighborhood_fields)
  def get(self):
    return  NeighborhoodModel.query.all()



class NeighborhoodApi(Resource):
  @marshal_with(neighborhood_fields)
  def get(self, name):
    print(name )
    return  NeighborhoodModel.query.filter_by(name=name ).all()
class NeighborhoodAreaApi(Resource):
  #@marshal_with(neighborhood_area_fields)
  def get(self, name):
    print(name )
    query = NeighborhoodModel.query.with_entities(NeighborhoodModel.name,NeighborhoodModel.geom.ST_Buffer(2).ST_Area().label('bufferarea')).all() #.filter_by(name=name ).all()
    return ['%s: %f' % (row.name, row.bufferarea) for row in query]




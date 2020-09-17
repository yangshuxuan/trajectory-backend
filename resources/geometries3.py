from flask import request
from database.postsqldb.models import Geometries3Model

from database.postsqldb.db import db

from flask_restful import Resource,  marshal_with
from database.postsqldb.models import neighborhood_fields,neighborhood_area_fields


class Geometries3sApi(Resource):
  #@marshal_with(neighborhood_fields)
  def get(self):
    #query = Geometries3Model.query.with_entities(Geometries3Model.name,Geometries3Model.geom.ST_AsText ().label('bufferarea')).all()
    query = Geometries3Model.query.with_entities(Geometries3Model.name,Geometries3Model.geom.ST_StartPoint().ST_M ().label('bufferarea')).all()
    #query = Geometries3Model.query.with_entities(Geometries3Model.name,Geometries3Model.geom.label('bufferarea')).all()
    
    return ['%s: %s' % (row.name, row.bufferarea) for row in query]
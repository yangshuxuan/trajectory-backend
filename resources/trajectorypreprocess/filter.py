from database.postsqldb.trajectorypreprocess.trajectoryfiltermodel import ObjectTrajactoryAfterFilterModel
from flask_restful import Resource
from database.postsqldb.models import ObjectTrajactoryModel
class ObjectTrajactoryFilterApi(Resource):
  def get(self,id):
    p = ObjectTrajactoryAfterFilterModel.query.get(id)
    if p is None:
        p = ObjectTrajactoryModel.query.get(id)

    return p.dictRepr(),200
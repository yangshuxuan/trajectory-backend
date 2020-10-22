from database.postsqldb.trajectorypreprocess.trajectoryfiltermodel import ObjectTrajactoryAfterFilterModel
from flask_restful import Resource
from database.postsqldb.models import ObjectTrajactoryModel
class ObjectTrajactoryFilterApi(Resource):

  def get(self,id):
    """
    
    """
    p = ObjectTrajactoryAfterFilterModel.trajectoryfilter(id)

    return p.dictRepr(),200
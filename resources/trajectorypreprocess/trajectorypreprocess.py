from database.postsqldb.trajectorypreprocess.trajectorypreprocessmodel import ObjectTrajactoryAfterFilterModel,ObjectTrajactoryAfterSegmentModel
from flask_restful import Resource
from database.postsqldb.models import ObjectTrajactoryModel
class ObjectTrajactoryFilterApi(Resource):

  def get(self,id):
    """
    
    """
    p = ObjectTrajactoryAfterFilterModel.trajectoryfilter(id)

    return p.dictRepr(),200


class ObjectTrajactorySegmentsApi(Resource):

  def get(self,id):
    """
    
    """
    rows = ObjectTrajactoryAfterSegmentModel.trajectorysegment(id)

    return [p.dictRepr() for p in rows],200
from database.postsqldb.trajectorypreprocess.trajectorypreprocessmodel import ObjectTrajactoryAfterFilterModel,ObjectTrajactoryAfterSegmentModel
from flask_restful import Resource
from database.postsqldb.models import ObjectTrajactoryModel
from flask_restful import reqparse
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
    parser = reqparse.RequestParser()

    parser.add_argument('max_turn_radius',type=float)
    
    args = parser.parse_args()

    max_turn_radius = args['max_turn_radius']

    max_turn_radius = max_turn_radius  if max_turn_radius is not None else 10.0

    #print("max_turn_radius={}".format(max_turn_radius))
    
    rows = ObjectTrajactoryAfterSegmentModel.trajectorysegment(id,max_turn_radius)

    return [p.dictRepr() for p in rows],200

from .car import CarsApi,CarApi
from .neighborhood import NeighborhoodApi,NeighborhoodsApi,NeighborhoodAreaApi
from .geometries3 import Geometries3sApi
from .lastappeared import LastappearedApi,LastappearedsApi,LastappearedsFilterApi
from .objecttrajactory import ObjectTrajactorysApi,ObjectTrajactoryApi,ObjectTrajactoryPredictorApi,SimilarObjectTrajactorysApi,ObjectTrajectoryLastNminutesApi
from .exceptioninfo import ExceptionInfosApi
def initialize_routes(api):
 
 
    api.add_resource(CarsApi, '/cars')
    api.add_resource(CarApi, '/cars/<int:id>')

    api.add_resource(NeighborhoodsApi,'/neighborhoods')
    api.add_resource(NeighborhoodApi,'/neighborhoods/<string:name>')
    api.add_resource(NeighborhoodAreaApi, '/neighborhoods/area/<string:name>')

    api.add_resource(Geometries3sApi,'/geometries3s')

    api.add_resource(LastappearedsApi,'/lastappeared')
    api.add_resource(LastappearedApi, '/lastappeared/<id>')
    api.add_resource(LastappearedApi, '/objectdetail/<id>',endpoint="transform_lastappearedapi_for_objectdetail")
    api.add_resource(ObjectTrajactorysApi,'/objecttrajactory')
    api.add_resource(ObjectTrajactoryApi,'/objecttrajactory/<id>')
    api.add_resource(ObjectTrajactoryPredictorApi,'/objecttrajactorypredictor/<id>')
    api.add_resource(LastappearedsFilterApi,'/lastappearedfilter')

    api.add_resource(ObjectTrajectoryLastNminutesApi, '/objecttrajactory/lastnminutes/<int:minutes>')
    api.add_resource(ExceptionInfosApi, '/exceptioninfo')

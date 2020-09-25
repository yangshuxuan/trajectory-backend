
from .car import CarsApi,CarApi
from .neighborhood import NeighborhoodApi,NeighborhoodsApi,NeighborhoodAreaApi
from .geometries3 import Geometries3sApi
from .lastappeared import LastappearedApi,LastappearedsApi
from .objecttrajactory import ObjectTrajactorysApi,ObjectTrajactoryApi
def initialize_routes(api):
 
 
 api.add_resource(CarsApi, '/cars')
 api.add_resource(CarApi, '/cars/<int:id>')

 api.add_resource(NeighborhoodsApi,'/neighborhoods')
 api.add_resource(NeighborhoodApi,'/neighborhoods/<string:name>')
 api.add_resource(NeighborhoodAreaApi, '/neighborhoods/area/<string:name>')

 api.add_resource(Geometries3sApi,'/geometries3s')

 api.add_resource(LastappearedsApi,'/lastappeared')
 api.add_resource(LastappearedApi, '/lastappeared/<id>')
 api.add_resource(ObjectTrajactorysApi,'/objecttrajactory')
 api.add_resource(ObjectTrajactoryApi,'/objecttrajactory/<id>')
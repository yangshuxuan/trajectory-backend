
from .car import CarsApi,CarApi
from .neighborhood import NeighborhoodApi,NeighborhoodsApi,NeighborhoodAreaApi

def initialize_routes(api):
 
 
 api.add_resource(CarsApi, '/cars')
 api.add_resource(CarApi, '/cars/<int:id>')

 api.add_resource(NeighborhoodsApi,'/neighborhoods')
 api.add_resource(NeighborhoodApi,'/neighborhoods/<string:name>')
 api.add_resource(NeighborhoodAreaApi, '/neighborhoods/area/<string:name>')


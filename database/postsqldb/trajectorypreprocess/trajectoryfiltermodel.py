from database.postsqldb.db import db
from database.postsqldb.models import TrajectoryMixin
class ObjectTrajactoryAfterFilterModel(TrajectoryMixin,db.Model):
    __tablename__ = 'objecttrajactoryafterfilter'
        
    
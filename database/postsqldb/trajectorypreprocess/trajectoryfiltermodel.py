from database.postsqldb.db import db
from database.postsqldb.models import TrajectoryMixin,ObjectTrajactoryModel
class ObjectTrajactoryAfterFilterModel(TrajectoryMixin,db.Model):
    __tablename__ = 'objecttrajactoryafterfilter'

    @staticmethod
    def trajectoryfilter(id):
        """
        首先从该表objecttrajactoryafterfilter获取该id对应的已经处理好的轨迹
        如果没有，则从表objecttrajactory获取该id的对应的原始轨迹，
        然后使用滤波器对原始轨迹处理并保存到表objecttrajactoryafterfilter，并将处理好的轨迹返回给用户
        要求：仿真一个毛刺轨迹，处理以后变平滑
        """
        p = ObjectTrajactoryAfterFilterModel.query.get(id)
        if p is None:
            p = ObjectTrajactoryModel.query.get(id)
            # please do something here


        return p
    
    
        
    
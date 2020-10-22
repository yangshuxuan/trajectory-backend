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
    
    
        
class ObjectTrajactoryAfterSegmentModel(TrajectoryMixin,db.Model):
    __tablename__ = 'objecttrajactoryaftersegments'
    segment_id = db.Column(db.Integer, nullable=False,primary_key=True)
    def dictRepr(self,**kwargs):
        d = super().dictRepr(**kwargs)
        d["segment_id"] = self.segment_id
        return d
    
    @staticmethod
    def trajectorysegment(id):
        """
        技术需求：按用户设定的转弯半径阈值，将轨迹分段。
        首先从该表objecttrajactoryaftersegments获取该id对应的已经处理好的所有轨迹段
        如果没有，则从表objecttrajactory获取该id的对应的原始轨迹，
        然后使用分段算法对原始轨迹处理并保存到表objecttrajactoryaftersegments，并将处理好的轨迹分段返回给用户
        要求：仿真一个至少有三个转弯的轨迹，通过该算法分成四段
        """
        
        p = ObjectTrajactoryAfterSegmentModel.query.filter_by(lastappeared_id=id).all() ## 这应该返回的是数组
        if p is None:
            p = ObjectTrajactoryModel.query.get(id)
            # please do something here
            # segement the trajectory to several parts,save these parts to objecttrajactoryaftersegments ,return them


        return p    
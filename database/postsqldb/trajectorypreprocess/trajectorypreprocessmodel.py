from database.postsqldb.db import db
from database.postsqldb.models import TrajectoryMixin,ObjectTrajactoryModel
from datetime import datetime
class TrajectoryMixinWithLastmodifiedDateTime(TrajectoryMixin):
    lastmodified_datetime = db.Column(db.DateTime, nullable=False,default=datetime.now)
    def dictRepr(self,**kwargs):
       
        d = super().dictRepr(**kwargs)
        d["lastmodified_datetime"] = self.lastmodified_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return d
class ObjectTrajactoryAfterFilterModel(TrajectoryMixinWithLastmodifiedDateTime,db.Model):
    __tablename__ = 'objecttrajactoryafterfilter'

    @staticmethod
    def trajectoryfilter(id):
        """
        首先从该表objecttrajactoryafterfilter获取该id对应的已经处理好的轨迹
        如果没有，则从表objecttrajactory获取该id的对应的原始轨迹，
        然后使用滤波器对原始轨迹处理并保存到表objecttrajactoryafterfilter，并将处理好的轨迹返回给用户
        如果有，需要比较最近更新时间，如果有变化，也需要重新计算
        要求：仿真一个毛刺轨迹，处理以后变平滑
        """
        p = ObjectTrajactoryAfterFilterModel.query.get(id)
        if p is None:
            p = ObjectTrajactoryModel.query.get(id)
            # please do something here


        return p
    
    
        
class ObjectTrajactoryAfterSegmentModel(TrajectoryMixinWithLastmodifiedDateTime,db.Model):
    __tablename__ = 'objecttrajactoryaftersegments'
    segment_id = db.Column(db.Integer, nullable=False,primary_key=True)
    max_turn_radius = db.Column(db.Float, nullable=False) #最大转弯半径阈值
    real_turn_radius = db.Column(db.Float, nullable=False) # 实际转弯半径
    lastmodified_datetime = db.Column(db.DateTime, nullable=False,default=datetime.now) #最近分段时间
    def dictRepr(self,**kwargs):
        d = super().dictRepr(**kwargs)
        d["segment_id"] = self.segment_id
        d["max_turn_radius"] = self.max_turn_radius
        d["real_turn_radius"] = self.real_turn_radius
        return d
    
    @staticmethod
    def trajectorysegment(id,max_turn_radius=10.0):
        """
        技术需求：按用户设定的转弯半径阈值，将轨迹分段。
        首先从该表objecttrajactoryaftersegments获取该id对应的已经处理好的所有轨迹段
        如果没有，则从表objecttrajactory获取该id的对应的原始轨迹，
        然后使用分段算法对原始轨迹处理并保存到表objecttrajactoryaftersegments，并将处理好的轨迹分段返回给用户
        如果有，需要比较最近更新时间和转弯半径阈值，如果有变化，也需要重新计算
        要求：仿真一个至少有三个转弯的轨迹，通过该算法分成四段
        """
        
        p = ObjectTrajactoryAfterSegmentModel.query.filter_by(lastappeared_id=id).all() ## 这应该返回的是数组
        if p is None:
            p = ObjectTrajactoryModel.query.get(id)
            # please do something here
            # segement the trajectory to several parts,save these parts to objecttrajactoryaftersegments ,return them


        return p    
# -*- coding: utf-8 -*-
# @Author  : zhang35
# @Time    : 2020/10/15 14:25
# @Function:
from database.postsqldb.db import db
from datetime import datetime
from geoalchemy2.types import Geometry
from flask_restful import fields
from geoalchemy2.elements import WKTElement
from statsmodels.tsa.statespace.varmax import VARMAX
from random import random
class ExceptionInfoModel(db.Model):
    __tablename__ = 'exceptioninfo'
    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.String(50))
    exception_type = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=False)

    def update(self, info):
        self.end_time = info["end_time"]
        self.reason = info["reason"]
    def dictRepr(self):
        info = {
                "id": self.id,
                "object_id": self.object_id,
                "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "exception_type": self.exception_type,
                "reason": self.reason
                }

        return info

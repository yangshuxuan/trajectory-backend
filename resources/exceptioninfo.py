# -*- coding: utf-8 -*-
# @Author  : zhang35
# @Time    : 2020/10/15 14:14
# @Function: exceptioninfo table api

from flask import request
from database.postsqldb.exceptionInfoModel import ExceptionInfoModel
from database.postsqldb.db import db

from flask_restful import Resource, reqparse

class ExceptionInfoApi(Resource):
    def get(self, id):
        rows = ExceptionInfoModel.query.filter_by(object_id=id)
        return [row.dictRepr() for row in rows]
    def put(self, id):
        body = request.get_json()
        body["id"] = id
        exceptionInfo = ExceptionInfoModel(**body)
        db.session.add(exceptionInfo)
        db.session.commit()
        return {'id': exceptionInfo.id}
class ExceptionInfosApi(Resource):
    def get(self):
        rows = ExceptionInfoModel.query.all()
        return [row.dictRepr() for row in rows]

    # 更新object_id和start_time均相同的条目，若没有均相同的，则新建
    def put(self):
        body = request.get_json()
        for info in body:
            exceptionInfoModel = ExceptionInfoModel.query\
                .filter(ExceptionInfoModel.object_id==info["object_id"],
                        ExceptionInfoModel.start_time==info["start_time"])\
                .first()
            if exceptionInfoModel is None:
                exceptionInfoModel = ExceptionInfoModel(**info)
                db.session.add(exceptionInfoModel)
            else:
                exceptionInfoModel.update(info)
        db.session.commit()
        return str(len(body))+" items updated", 200
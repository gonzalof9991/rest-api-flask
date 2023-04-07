import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import  Blueprint, abort
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema, StoreUpdateSchema

"""
Blueprint en Flask Smallest se utiliza para dividir una API en multiples segmentos
"""
blp = Blueprint("Stores","stores", description="Operations on stores")

"""
MethodView -> Podemos crear una clase cuyos métodos se dirijan a un punto final específico.
"""
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        # query.get_or_404 -> va a buscar a la BD con la clave primaria que le pasamos y si no encuentra nada retorna un 404
        store = StoreModel.query.get_or_404(store_id)
        return store
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted"}

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self,store_data,store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Updating an store is not implemented.")

@blp.route("/store/")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error ocurred whilte inserting the store.")
        return store

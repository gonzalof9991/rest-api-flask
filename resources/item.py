import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt
from db import db

"""
Blueprint en Flask Smallest se utiliza para dividir una API en multiples segmentos
"""
blp = Blueprint("Items", "items", description="Operations on items")

"""
MethodView -> Podemos crear una clase cuyos métodos se dirijan a un punto final específico.
"""


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        # query.get_or_404 -> va a buscar a la BD con la clave primaria que le pasamos y si no encuentra nada retorna
        # un 404
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            item.description = item_data["description"]
        else:
            item = ItemModel(id=item_id, **item_data)
        """
        -> Una forma de comunicar al usuario que esto no se ha hecho todavía
        raise NotImplementedError("Updating an item is not implemented.")
        """
        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item/")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # Decorador para Schema
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred whilte inserting the item.")
        return item




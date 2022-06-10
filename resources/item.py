from typing import Tuple

import sqlite3

from models.item import ItemModel

from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be blank!'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item need a store id.'
    )

    @jwt_required()
    def get(self, name: str) -> Tuple:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    @staticmethod
    def post(name: str) -> Tuple:
        if ItemModel.find_by_name(name):
            return {'message': f"An item with the name, '{name}' already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except sqlite3.Error:
            return {'message': "An error occurred while inserting the item."}, 500  # internal server error

        return item.json(), 201

    @staticmethod
    def delete(name: str) -> Tuple:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': f"Item, {name} deleted"}, 200

    @staticmethod
    def put(name: str) -> Tuple:
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except sqlite3.Error:
                return {'message': "An error occurred while inserting the item."}, 500
        else:
            try:
                item.price, item.store_id = data.values()
            except sqlite3.Error:
                return {'message': "An error occurred while updating the item."}, 500
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):

    def get(self) -> Tuple:
        return {'items': [item.json() for item in ItemModel.query.all()]}

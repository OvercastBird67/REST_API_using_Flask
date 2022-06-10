import sqlite3
from flask_restful import Resource
from sqlalchemy import delete
from models.store import StoreModel


class Store(Resource):

    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message': 'Store not found'}, 404

    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {'message': f"A store with name {name} already exists."}, 404
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except sqlite3.Error:
            return {'message': 'An error occured while creating the store'}, 500
        
        return store.json(), 201

    def delete(self, name: str):
        if (store := StoreModel.find_by_name(name)):
            store.delete_from_db()
        
        return {'message': 'Store deleted'}, 200


class StoreList(Resource):
    
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

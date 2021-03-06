from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is not None:
            store.delete_from_db()
            return {'message': 'Store deleted'}, 200
        else:
            return {'message': 'Store not deleted'}, 404


class StoreList(Resource):
    @jwt_required()
    def get(self):
        stores = []
        for store in StoreModel.query.all():
            stores.append(store.json())

        return {'stores': stores}

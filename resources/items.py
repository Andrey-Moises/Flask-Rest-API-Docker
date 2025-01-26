from   db                 import db
from   sqlalchemy.exc     import SQLAlchemyError
from   models             import ItemModel
from   flask              import request
from   schemas            import ItemSchema, ItemUpdateSchema
from   flask.views        import MethodView
from   flask_smorest      import Blueprint, abort
from   flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint('items', __name__, description='Items operations')

@blp.route('/item/<string:item_id>')
class Items(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id) # Automatically aborts if item is not found
        return item
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(403, message="Admin access required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):

        item = ItemModel.query.get(item_id)

        if item:
            item.name     = item_data.get('name', item.name)
            item.price    = item_data.get('price', item.price)
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
    
@blp.route('/item')
class ItemsList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required() # Requires a valid JWT token
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return item

from flask.views    import MethodView
from flask_smorest  import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db             import db
from models         import TagModel, StoreModel, ItemModel
from schemas        import TagSchema, TagAndItemsSchema

blp = Blueprint('Tags', __name__, description='Tags for stores')

@blp.route('/store/<string:store_id>/tag')
class TagsInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()


    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        if TagModel.query.filter_by(name=tag_data['name'], store_id=store_id).first(): # Check if a tag with the same name already exists
            abort(400, message="A tag with the same name already exists")
        
        store = StoreModel.query.get_or_404(store_id)
        tag   = TagModel(**tag_data)
        tag.store = store

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A tag with the same name already exists")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500)

        return tag
    
@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagToItem(MethodView):

    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):

        tag  = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        if tag in item.tags:
            abort(400, message="Tag already linked to item")

        item.tags.append(tag)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Internal server error")
        
        return tag
        
    @blp.response(201, TagAndItemsSchema)
    def delete(self, item_id, tag_id):

        tag  = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        try:
            if tag in item.tags:
                item.tags.remove(tag)
                db.session.add(item)
                db.session.commit()
                return {"message": "Tag removed from item", "items": [item], "tags": [tag]}
            else:
                abort(404, message="Tag not found in item")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Internal server error")
            

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)

    @blp.response(202, description="Tag deleted", example={"message": "Tag deleted"})
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="Returned if the tag is linked to an item, the tag must be removed from the item first")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(400, message="Tag is linked to an item, remove the tag from the item first")
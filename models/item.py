from db import db


class ItemModel(db.Model):

    __tablename__ = 'items'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price    = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store    = db.relationship("StoreModel", back_populates="items") # back_populates is used to specify the relationship in the other model
    tags     = db.relationship("TagModel", back_populates="items", secondary="items_tags") # secondary is used to specify the association table
from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    
    id       = fields.Int(dump_only=True) # dump_only=True means that this field will not be included in the output
    name     = fields.Str(required=True) # required=True means that this field is required
    price    = fields.Float(required=True)

class PlainStoreSchema(Schema):
    
    id   = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    
    name     = fields.Str()
    price    = fields.Float()
    store_id = fields.Int()


class PlainTagSchema(Schema):
    
    id   = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class StoreSchema(PlainStoreSchema):
    
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True)) # List means that this field is a list of nested objects
    tags  = fields.List(fields.Nested(PlainTagSchema(), dump_only=True)) # List means that this field is a list of nested objects

class TagSchema(PlainTagSchema):

    store_id = fields.Int(load_only=True)
    store    = fields.Nested(PlainStoreSchema(), dump_only=True)
    items    = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))

class ItemSchema(PlainItemSchema):
    
    store_id = fields.Int(required=True, load_only=True) # load_only=True means that this field will not be included in the output
    store    = fields.Nested(PlainStoreSchema(), dump_only=True) # Nested means that this field is a nested object
    tags     = fields.List(fields.Nested(PlainTagSchema(), dump_only=True) ) # List means that this field is a list of nested objects

class TagAndItemsSchema(Schema):
    
    message = fields.Str()
    items   = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
    tags    = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))

class UserSchema(Schema):

    id       = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) # load_only=True means that this field will not be included in the output
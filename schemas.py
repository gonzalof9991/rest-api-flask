from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)  # No se va a usar para la validación
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(dump_only=True)  # No se va a usar para la validación


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    description = fields.Str()

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)  # No se va a usar para la validación
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Str(dump_only=True)  # No se va a usar para la validación
    name = fields.Str(required=True)


class StoreUpdateSchema(Schema):
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # Nunca se debe devolver la contraseña del usuario cuando se devuelve una información
    password = fields.Str(required=True, load_only=True)

from marshmallow import Schema, fields, EXCLUDE


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, data_key='uid',
                    example="f52706c8-ac08-4f9d-a092-8038d1769825")
    name = fields.Str(example="Jaime Arango")
    email = fields.Str(example="jarango@ops.servagro.com.co")
    attributes = fields.Mapping()
    authorization = fields.Mapping()

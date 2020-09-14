from marshmallow import Schema, fields
from .entity import EntitySchema


class MediaSchema(EntitySchema):
    name = fields.Str(
        required=False, example="company_logo")
    type = fields.Str(
        required=True, example="images")
    namespace = fields.Str(
        required=False, example="https://example.com")
    extension = fields.Str(
        required=True, example="png")
    reference = fields.Str(
        required=True, example="00648c29-eca2-4112-8a1a-4deedb443188")
    url = fields.Str(
        required=False, example=("https://mediark.knowark/media/images/"
                                 "00648c29-eca2-4112-8a1a-4deedb443188.jpg"))
    data = fields.Str(required=True, example="aGVsbG8=")

from marshmallow import Schema, fields
from .entity import EntitySchema


class MediaSchema(EntitySchema):
    name = fields.Str(example="company_logo")
    type = fields.Str(example="images")
    namespace = fields.Str(example="https://example.com")
    extension = fields.Str(example="png")
    reference = fields.Str(example="00648c29-eca2-4112-8a1a-4deedb443188")
    path = fields.Str(example=("images/custom/file/path.jpg"))
    url = fields.Str(example=("https://mediark.knowark/media/images/"
                              "00648c29-eca2-4112-8a1a-4deedb443188.jpg"))
    data = fields.Str(example="aGVsbG8=")

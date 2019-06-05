from marshmallow import Schema, fields

class ImageSchema(Schema):
    id = fields.Str(
        required=False, example="637250d6-dc57-4d96-9f8a-2697ca5c55c3")
    namespace = fields.Str(
        required=False, example="https://example.com")
    extension = fields.Str(
        required=False, example="png")
    reference = fields.Str(
        required=False, example="00648c29-eca2-4112-8a1a-4deedb443188")
    uri = fields.Str(
        requiered=False, example="https://mediark.knowark/media/images/00648c29-eca2-4112-8a1a-4deedb443188.jpg"
    )
    data = fields.Str(requiered=True, example="aGVsbG8=")

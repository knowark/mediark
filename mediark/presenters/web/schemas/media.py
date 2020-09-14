from marshmallow import Schema, fields


class MediaSchema(Schema):
    id = fields.Str(
        required=False, example="637250d6-dc57-4d96-9f8a-2697ca5c55c3")
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

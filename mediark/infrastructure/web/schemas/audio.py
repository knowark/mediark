from marshmallow import Schema, fields

class AudioSchema(Schema):
    id = fields.Str(
        required=False, example="637250d6-dc57-4d96-9f8a-2697ca5c55c3")
    namespace = fields.Str(
        required=False, example="https://example.com")
    extension = fields.Str(
        required=True, example="webm")
    reference = fields.Str(
        required=True, example="00648c29-eca2-4112-8a1a-4deedb443188")
    url = fields.Str(
        requiered=False, example="https://mediark.knowark/media/audios/00648c29-eca2-4112-8a1a-4deedb443188.webm"
    )
    data = fields.Str(requiered=True, example="aGVsbG8=")
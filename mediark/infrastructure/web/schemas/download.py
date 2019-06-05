from marshmallow import Schema, fields

class DownloadSchema(Schema):
   reference = fields.Str(
        required=True, example="00648c29-eca2-4112-8a1a-4deedb443188")
   type = fields.Str(
        requiered=True, example="audio")
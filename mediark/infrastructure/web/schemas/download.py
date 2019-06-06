from marshmallow import Schema, fields

class DownloadSchema(Schema):
     type = fields.Str(
        requiered=True, example="audio")
     reference = fields.Str(
          required=True, example="00648c29-eca2-4112-8a1a-4deedb443188")
     url = fields.Str(
          requiered=False, example="https://mediark.knowark/media/audios/00648c29-eca2-4112-8a1a-4deedb443188.webm"
     )

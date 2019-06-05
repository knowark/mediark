from marshmallow import Schema, fields

class DownloadSchema(Schema):
   pass


 # Download Resource
        # api.add_resource(DownloadResource,
        #                  '/download/<string:type>/<path:uri>',
        #                  resource_class_kwargs={
        #                      'MEDIA_DIRECTORY': app.config['MEDIA']})
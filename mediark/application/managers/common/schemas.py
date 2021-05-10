
entity_schema = {
    'id': str,
    'created_at:=createdAt': int,
    'created_by:=createdBy': str,
    'updated_at:=updatedAt': int,
    'updated_by:=updatedBy': str
}

media_schema = {**entity_schema, **{
    'name': str,
    'type': str,
    'size': int,
    'sequence': int,
    'reference': str,
    'path': str
}}

submission_schema = {
    'media': media_schema,
    'stream': (lambda v: (v is None or hasattr(v, 'read'))
               and v or ValueError(f'Invalid stream: {v}'))
}

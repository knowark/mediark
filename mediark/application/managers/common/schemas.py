
entity = {
    'id': str,
    'created_at:=createdAt': int,
    'created_by:=createdBy': str,
    'updated_at:=updatedAt': int,
    'updated_by:=updatedBy': str
}

media = {**entity, **{
    'name': str,
    'type': str,
    'namespace': str,
    'extension': str,
    'reference': str,
    'path': str,
    'url': str,
    'data': str
}}

submission = {
    'media': media,
    'stream': (lambda v: (v is None or hasattr(v, 'read'))
               and v or ValueError(f'Invalid stream: {v}'))
}

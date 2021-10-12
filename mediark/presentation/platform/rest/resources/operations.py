def operations():
    return {
        # Media
        'mediaHeadId': {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.count',
                    'meta': {'model': 'Media'}
                 }
             }
        },
        "mediaGetId": {
            'actions':{
                'default':{
                    'handler': 'StandardInformer.search',
                    'meta': {'model': 'Media'}
                }
            }
        },
        'mediaPatchId': {
            'actions':{
                'default':{
                    'handler': 'MediaStorageManager.submit',
                    'meta': {'model': 'Media'}
                }
            }
        },
        'mediaDeleteId': {
            'actions':{
                'default':{
                    'handler': 'StandardManager.remove',
                    'meta': {'model': 'Media'}
                }
            }
        },
        'emailPatchId': {
            'actions':{
                'default':{
                    'handler': 'EmailManager.request',
                    'meta': {'model': 'Email'}
                }
            }
        }
    }


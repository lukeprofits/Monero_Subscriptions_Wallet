config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default'
        }
    },
    'loggers': {
        'src.rpc_server': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'src.rpc_client': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'src.rpc_config': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}
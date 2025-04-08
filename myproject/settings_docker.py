import os

from .settings import *

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Enable debug mode temporarily to see detailed error messages
DEBUG = True

# Allow all hosts for now
ALLOWED_HOSTS = ['*']

# Database settings for MongoDB Atlas
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ec2',
        'CLIENT': {
            'host': 'mongodb+srv://tranhung10122003:OJw5AywNkq2TBQOw@cluster0.24wivb9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
            'username': 'tranhung10122003',
            'password': 'OJw5AywNkq2TBQOw',
            'authSource': 'admin',
        },
    }
}

# Add detailed logging to see what's happening
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}
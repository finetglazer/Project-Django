import os

from .settings import *

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Set debug to False in production
DEBUG = False

# Allow all hosts for now (customize this for production)
ALLOWED_HOSTS = ['*']

# Database settings - use environment variables

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ec2',  # You can specify the database name here
        'CLIENT': {
            'host': 'mongodb+srv://tranhung10122003:OJw5AywNkq2TBQOw@cluster0.24wivb9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
            'username': 'tranhung10122003',  # Your MongoDB username (from Atlas)
            'password': 'OJw5AywNkq2TBQOw',  # Your MongoDB password (replace <db_password> with the actual password)
            'authSource': 'admin',  # MongoDB authentication source (usually 'admin')
        },
    }
}
DATABASES = {

	'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'time_base',
        'OPTIONS': {
    }

   'mongodb': {
      'ENGINE': 'django_mongodb_engine',
      'NAME': 'graphos_mongo'
   }
}

GRAPHOS_DEFAULT_DATABASE = "model" # mongodb, sqlite3, redis
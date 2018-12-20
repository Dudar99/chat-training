


try:
    from .local_config import *
except EnvironmentError:
    pass

DATABASE = {
    'POSTGRES_USER': LOCAL_DB_SETTINGS['POSTGRES_USER'],
    'POSTGRES_PASSWORD': LOCAL_DB_SETTINGS['POSTGRES_PASSWORD'],
    'HOST': LOCAL_DB_SETTINGS['HOST'],
    'PORT': LOCAL_DB_SETTINGS['PORT'],
    'DB_NAME': LOCAL_DB_SETTINGS['DB_NAME']
}

from distutils.debug import DEBUG

from flask_sqlalchemy import SQLAlchemy


class developmentConfig:
    DEBUG = True                                                                    ### Activamos el depurador para poder ver los cambios en tiempo real
    SQLALCHEMY_TRACK_MODIFICATIONS = False                                          ### Pasamos la configuración: donde está la base de datos a la instancia de app
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/flaskmysql'           ### desactivamos los alerts que vienen por defecto """
                            ## mysql+pymysql://usuario@ip/nombre de la DB ###
    
config = {
    "development":developmentConfig
}
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ❗ Esta será la configuración por defecto (SQLite para desarrollo)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# OPCIONAL: configuración alterna si luego querés volver a SQL Server
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://daren:12345@localhost\\SQLEXPRESS01/Aerolinea?driver=ODBC+Driver+17+for+SQL+Server'
    )
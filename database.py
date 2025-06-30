from sqlalchemy import create_engine#creo la conexion a la base de datos
from sqlalchemy.orm import sessionmaker, declarative_base#creo la sesion para leer y escribir en la bd y el punto de partida para definir mis clases(modelos) como tablas

#defino la url de conexion para postgres
DATABASE_URL = "postgresql+psycopg2://postgres:Contrase%C3%B1a123%21@localhost:5432/ambientes"


#Motores de conexion
engine = create_engine(DATABASE_URL)#crea el motor de conexion lo usa sqlalchemy para comunicarse con poistgres

#Sesiones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)#defino como se crean las sesiones de base de datos 


#Base para cada entidad
Base = declarative_base()#punto de partida para declarar modelos





from sqlalchemy import Column, Integer, String,Float
from database import Base

#DEFINO LA TABLA USUARIOS EN MI BASE DE DATOS
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="admin")  # Opcional

#DEFINO LA TABLA CLIENTES EN MI BASE DE DATOS
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100))
    telefono=Column(String(100))
    contenido = Column(String(500))

#DEFINO LA TABLA SERVICIOS EN MI BASE DE DATOS
class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    
#DEFINO LA TABLA PRODUCTOS EN MI BASE DE DATOS
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio = Column(Float, nullable=False)    
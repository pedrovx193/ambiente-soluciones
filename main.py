from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles # sirve archivos css, js y mas desde /static
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Cliente, Usuario,Servicio as ServicioDB,Producto as ProductoDB
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from models import Cliente
from pydantic import BaseModel  # para JSON login
import smtplib
import ssl
import os
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from typing import List
#from fastapi import Path
# SQLAlchemy(ServicioDB) es para la tabla y  esquema Pydantic (Servicio) es para el esquema de validacion

# --- Seguridad ---
# -- Crea un contexto de contraseñas usando el algoritmo bcrypt para guardar la contraseña
pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "clavesecreta" #define una clave secreta para firmar los jwt. 
ALGORITHM = "HS256" #algoritmo criptografico para firmas los tokens jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # es el tiempo de expiracion del token despued de ello se debe reiniciar la sesion, el token lo genera el backend


# --- Inicializar Base de Datos ---
#load_dotenv()#carga laas variables de entorno desde mi archivo.env
Base.metadata.create_all(bind=engine)#creo todas las tablas de mi base de datos segun models.py
print("¡Base de datos inicializada!")#Me indica que la base de datos esta lista

# --- App ---
app = FastAPI()#creo mio servidor web, esto lo paso a uvicorn main:app --reload para ejecutarlo

app.mount("/static", StaticFiles(directory="static"), name="static")#publico o sirvo archivos estaticos de /static
templates = Jinja2Templates(directory="templates")#carpeta en donde guardo mis archivos html dinamicos notacion jinja2{%}

# --- Dependencia DB ---
def get_db():#defino una funcion de dependencia para tener cx a mi bd
    db = SessionLocal()#creo una nueva sesion independiente en la bd verificar en database.py
    try:
        yield db # yield hace que la funcion sea un generador para abiir y cerrar recursos automaticamente 
    finally:
        db.close()#cerrar la sesion para evitar fugas de cx o sesiones abiertas

# --- Servicios en memoria ---
#servicios = []

class ServicioSchema(BaseModel):#defino un modelo de datos usando pydantic(basemodel) creo una clase pydantic llamada servicio
    nombre: str #atributo
    descripcion: str
    precio: float

# --- Modelo para Entrada de Servicio ---
class ServicioInput(BaseModel):#modelo de validacion para recibir datos en PUT O POST
    nombre: str
    descripcion: str
    precio: float
    
# --- Login JSON para Postman o /docs ---
class LoginInput(BaseModel):#modelo para recibir datos del login,en postman POST http://127.0.0.1:8000/api/login,JSON escribir "username":"admin" lo mismo para password y me devuelve el token jwt
    username: str
    password: str    
    
    
# --- Productos en memoria ---

class ProductoSchema(BaseModel):#defino un modelo de datos usando pydantic(basemodel) creo una clase pydantic llamada servicio
    nombre: str #atributo
    descripcion: str
    precio: float

# --- Modelo para Entrada de Productos ---
class ProductoInput(BaseModel):#modelo de validacion para recibir datos en PUT O POST
    nombre: str
    descripcion: str
    precio: float    
    
# --- Login JSON para Postman o /docs ---
class LoginInput(BaseModel):#modelo para recibir datos del login,en postman POST http://127.0.0.1:8000/api/login,JSON escribir "username":"admin" lo mismo para password y me devuelve el token jwt
    username: str
    password: str    
    
# --- Rutas HTTP GET  que se cargan y devuelven una pagina html ---    
@app.get("/", response_class=HTMLResponse) #Carga templates/ o la raiz
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/nosotros", response_class=HTMLResponse) #Carga templates/nosotros.html.
def read_nosotros(request: Request):
    return templates.TemplateResponse("nosotros.html", {"request": request})

#PUBLICO DINAMICAMENTE MIS SERVICIOS DESDE MI PAGINA DE ADMIN A LA PAGINA PRINCIPAL DE SERVICIOS
@app.get("/servicios", response_class=HTMLResponse)#consulto la bd de servicios y obtengo la lista de servicios guardados  Carga templates/servicios.html.
def read_servicios(request: Request, db: Session = Depends(get_db)):
    servicios = db.query(ServicioDB).all()
    return templates.TemplateResponse(
        "servicios.html",
        {"request": request, "servicios": servicios}
    )
    
#PUBLICO DINAMICAMENTE MIS PRODUCTOS DESDE MI PAGINA DE ADMIN A LA PAGINA PRINCIPAL DE PRODUCTOS
@app.get("/productos", response_class=HTMLResponse)#consulto la bd de productos y obtengo la lista de productos guardados  Carga templates/productos.html.
def read_productos(request: Request, db: Session = Depends(get_db)):
    productos = db.query(ProductoDB).all()
    return templates.TemplateResponse(
        "productos.html",
        {"request": request, "productos": productos}
    )  

@app.get("/contacto", response_class=HTMLResponse) #Carga templates/contactos.html.
async def contacto(request: Request):
    return templates.TemplateResponse("contacto.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)#Carga templates/login.html.
def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)#mustra la pagina admin solo si estas logueado
def read_admin(request: Request):
    # Si no existe la cookie "logueado", redirige a /login
    if request.cookies.get("logueado") != "si":
        return RedirectResponse(url="/login", status_code=303)
    # Si existe, carga la página de admin
    return templates.TemplateResponse("admin.html", {"request": request})



@app.get("/admin/clientes")
def consultar_clientes(request: Request, db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})

# --- Registro de Usuario ---

@app.post("/register")#defino al ruta HTTP POST en /register, la uso para registrar un usuario enviando datos desde un formulario HTML
def register(
    username: str = Form(...),#se lee del formulario usando Form
    password: str = Form(...),
    db: Session = Depends(get_db)#realiza la conexion a la base de datos
):
    hashed_password = pwd_context.hash(password)#tomo la contraseña del formulario y al convierto a un hash seguro usando bcrypt
    usuario = Usuario(username=username, hashed_password=hashed_password)#creo un objeto usuario 
    db.add(usuario)#lo agrego a la base de datos 
    try:
        db.commit()#guardo el usuario 
    except:#si falla
        db.rollback()#deahago la operacion con rolback
        raise HTTPException(status_code=400, detail="El usuario ya existe")#lanzo error
    return {"msg": "Usuario registrado correctamente"}


@app.post("/api/login")
def api_login(
    creds: LoginInput,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.username == creds.username).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if not pwd_context.verify(creds.password, usuario.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": usuario.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Login HTML con redirección a /admin ---
from fastapi.responses import RedirectResponse

@app.post("/login")
def login_html(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if not usuario:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuario no encontrado"})
    if not pwd_context.verify(password, usuario.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Contraseña incorrecta"})

    # Usuario válido → poner cookie y redirigir a /admin
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="logueado", value="si", max_age=3600)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("logueado")
    return response

# --- Formulario de Contacto ---

# --- REALIZO EL INGRESO Y ENVIO DE DATOS DESDE EL FORMULARIO CONTACTO---
@app.post("/enviar")
async def enviar_formulario(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono:str=Form(...),
    mensaje: str = Form(...)
):
    db = SessionLocal()
    nuevo_mensaje = Cliente(nombre=nombre, email=email, telefono=telefono,contenido=mensaje)
    db.add(nuevo_mensaje)
    db.commit()
    db.close()
    print("Mensaje guardado en la base de datos")

    # Usa url_for para que siempre redirija bien
    remitente = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receptor = remitente

    subject = f"Mensaje de {nombre} <{email}>"
    body = f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}"

    mensaje_email = f"Subject: {subject}\n\n{body}"

    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(remitente, password)
            server.sendmail(remitente, receptor, mensaje_email)
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error enviando correo: {e}")

    return RedirectResponse(url="/contacto", status_code=303)

# --- REALIZO LA CONSULTA DE LOS DATOS ENVIADOS DEL FORMULARIO SECCION CONTACTO ---
@app.get("/clientes")
async def get_clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    db.close()
    return JSONResponse(content=[{
        "id": m.id,
        "nombre": m.nombre,
        "email": m.email,
        "telefono":m.telefono,
        "contenido": m.contenido
    } for m in clientes])
   
       
# --- API Servicios ---
# --- API Servicios con Base de Datos ---
@app.post("/api/servicios")
def agregar_servicio(servicio: ServicioSchema, db: Session = Depends(get_db)):
    nuevo_servicio = ServicioDB(
        nombre=servicio.nombre,
        descripcion=servicio.descripcion,
        precio=servicio.precio
    )
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return {"mensaje": "Servicio agregado correctamente", "id": nuevo_servicio.id}

@app.get("/api/servicios")
def obtener_servicios(db: Session = Depends(get_db)):
    servicios = db.query(ServicioDB).all()
    return [
        {
            "id": s.id,
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "precio": s.precio
        }
        for s in servicios
    ]
    

# Eliminar servicio por ID
@app.delete("/api/servicios/{id}")
def eliminar_servicio(id: int, db: Session = Depends(get_db)):
    servicio = db.query(ServicioDB).filter(ServicioDB.id == id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.delete(servicio)
    db.commit()
    return {"mensaje": "Servicio eliminado correctamente"}

# Editar servicio por ID
@app.put("/api/servicios/{id}")
def editar_servicio(id: int, servicio_input: ServicioInput, db: Session = Depends(get_db)):
    servicio = db.query(ServicioDB).filter(ServicioDB.id == id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    servicio.nombre = servicio_input.nombre
    servicio.descripcion = servicio_input.descripcion
    servicio.precio = servicio_input.precio
    db.commit()
    return {"mensaje": "Servicio actualizado correctamente"}    


# --- API Productos ---
# --- API Productos con Base de Datos ---
@app.post("/api/productos")
def agregar_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    nuevo_producto = ProductoDB(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return {"mensaje": "Producto agregado correctamente", "id": nuevo_producto.id}

@app.get("/api/productos")
def obtener_productos(db: Session = Depends(get_db)):
    productos = db.query(ProductoDB).all()
    return [
        {
            "id": s.id,
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "precio": s.precio
        }
        for s in productos
    ]
    

# Eliminar producto por ID
@app.delete("/api/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto= db.query(ProductoDB).filter(ProductoDB.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado correctamente"}

# Editar producto por ID
@app.put("/api/productos/{id}")
def editar_producto(id: int, producto_input: ProductoInput, db: Session = Depends(get_db)):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.nombre = producto_input.nombre
    producto.descripcion = producto_input.descripcion
    producto.precio = producto_input.precio
    db.commit()
    return {"mensaje": "Producto actualizado correctamente"}    

   
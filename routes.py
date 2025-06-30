
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cliente, Cotizacion, Usuario
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/nosotros", response_class=HTMLResponse)
async def nosotros(request: Request):
    return templates.TemplateResponse("nosotros.html", {"request": request})

# Formularios
@router.post("/registro")
async def registro(nombre: str = Form(...), email: str = Form(...), telefono: str = Form(...), db: Session = Depends(get_db)):
    cliente = Cliente(nombre=nombre, email=email, telefono=telefono)
    db.add(cliente)
    db.commit()
    return RedirectResponse("/", status_code=303)

# Registro usuario
@router.post("/registro_usuario")
async def registro_usuario(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = Usuario(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=303)

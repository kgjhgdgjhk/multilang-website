from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import json
import os

from . import models, schemas, auth, database
from .database import get_db, init_db

# إنشاء التطبيق
app = FastAPI(title="MultiLang Website")

# تهيئة قاعدة البيانات
init_db()

# إعداد القوالب
templates = Jinja2Templates(directory="backend/templates")

# تركيبات المسارات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# تقديم الملفات الثابتة
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ترجمة النصوص
translations = {
    "en": {
        "welcome": "Welcome to our website",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "username": "Username",
        "password": "Password",
        "email": "Email",
        "full_name": "Full Name",
        "confirm_password": "Confirm Password",
        "submit": "Submit",
        "home": "Home",
        "profile": "Profile",
        "dashboard": "Dashboard",
        "language": "Language",
        "english": "English",
        "arabic": "Arabic",
        "french": "French",
        "spanish": "Spanish"
    },
    "ar": {
        "welcome": "مرحباً بكم في موقعنا",
        "login": "تسجيل الدخول",
        "register": "إنشاء حساب",
        "logout": "تسجيل الخروج",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "email": "البريد الإلكتروني",
        "full_name": "الاسم الكامل",
        "confirm_password": "تأكيد كلمة المرور",
        "submit": "إرسال",
        "home": "الرئيسية",
        "profile": "الملف الشخصي",
        "dashboard": "لوحة التحكم",
        "language": "اللغة",
        "english": "الإنجليزية",
        "arabic": "العربية",
        "french": "الفرنسية",
        "spanish": "الإسبانية"
    },
    "fr": {
        "welcome": "Bienvenue sur notre site",
        "login": "Connexion",
        "register": "S'inscrire",
        "logout": "Déconnexion",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "email": "Email",
        "full_name": "Nom complet",
        "confirm_password": "Confirmer le mot de passe",
        "submit": "Soumettre",
        "home": "Accueil",
        "profile": "Profil",
        "dashboard": "Tableau de bord",
        "language": "Langue",
        "english": "Anglais",
        "arabic": "Arabe",
        "french": "Français",
        "spanish": "Espagnol"
    },
    "es": {
        "welcome": "Bienvenido a nuestro sitio web",
        "login": "Iniciar sesión",
        "register": "Registrarse",
        "logout": "Cerrar sesión",
        "username": "Nombre de usuario",
        "password": "Contraseña",
        "email": "Correo electrónico",
        "full_name": "Nombre completo",
        "confirm_password": "Confirmar contraseña",
        "submit": "Enviar",
        "home": "Inicio",
        "profile": "Perfil",
        "dashboard": "Panel de control",
        "language": "Idioma",
        "english": "Inglés",
        "arabic": "Árabe",
        "french": "Francés",
        "spanish": "Español"
    }
}

# مسارات API
@app.get("/")
async def read_root(request: Request, lang: str = "en"):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "lang": lang,
        "translations": translations.get(lang, translations["en"])
    })

@app.get("/api/translations/{lang}")
async def get_translations(lang: str):
    return translations.get(lang, translations["en"])

@app.get("/login")
async def login_page(request: Request, lang: str = "en"):
    return templates.TemplateResponse("login.html", {
        "request": request, 
        "lang": lang,
        "translations": translations.get(lang, translations["en"])
    })

@app.post("/api/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # هنا يجب التحقق من بيانات المستخدم
    # هذا مثال مبسط
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user or not auth.verify_password(password, user.hashed_password):
        return JSONResponse(
            status_code=401,
            content={"message": "Invalid credentials"}
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.settings.access_token_expire_minutes)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/register")
async def register_page(request: Request, lang: str = "en"):
    return templates.TemplateResponse("register.html", {
        "request": request, 
        "lang": lang,
        "translations": translations.get(lang, translations["en"])
    })

@app.post("/api/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    # التحقق من وجود المستخدم مسبقاً
    existing_user = db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()
    
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"message": "Username or email already exists"}
        )
    
    # إنشاء مستخدم جديد
    hashed_password = auth.get_password_hash(password)
    db_user = models.User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        language=language
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully"}

@app.get("/dashboard")
async def dashboard(request: Request, lang: str = "en"):
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "lang": lang,
        "translations": translations.get(lang, translations["en"])
    })
# في نهاية main.py
if __name__ == "__main__":
    import uvicorn
    import os
    
    # على Render يأخذ المنفذ من متغير البيئة
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
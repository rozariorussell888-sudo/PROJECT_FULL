
"""
Django settings for My_Project.
ResourceLoop - Student Resource Sharing System
"""

import os
from pathlib import Path


                                            
                
                                            

BASE_DIR = Path(__file__).resolve().parent.parent


                                            
                   
                                            

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "development-only-change-before-deploy"
)

DEBUG = os.environ.get(
    "DJANGO_DEBUG", "True"
).lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "full-and-final.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://full-and-final.vercel.app",
]


                                            
                
                                            

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

                              
    "accounts",
    "resources",
    "requests_app",
]


                                            
            
                                            

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


                                            
                        
                                            

ROOT_URLCONF = "My_Project.urls"


                                            
                             
                                            

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                                                   
                "requests_app.context_processors.navbar_notifications",
            ],
        },
    },
]


                                            
      
                                            

WSGI_APPLICATION = "My_Project.wsgi.application"


                                            
                            
                                            

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


                                            
                     
                                            

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


                                            
                   
                                            

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


                                            
                               
                                            

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


                                            
                               
                                            

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"




                                            
                           
                                            

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465

EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

EMAIL_HOST_USER = "24101066@uap-bd.edu"

EMAIL_HOST_PASSWORD = "kjir gvnh brpz saoi"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 30
import os
"""
Django 설정 파일 (settings.py)

Django 5.1.5 버전으로 생성됨.
"""

from pathlib import Path

DEFAULT_CHARSET = 'utf-8'  # 기본 문자 인코딩을 UTF-8로 설정

# 프로젝트의 기본 디렉토리 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent


# 🚀 개발 환경 설정 (배포 시 반드시 수정 필요)

SECRET_KEY = 'django-insecure-9c*%_nfac&!6!_r6b#tnk1fr*2m3h3h-1p*usf0%shgv=v_s7d'  # 보안 키 (배포 환경에서는 숨겨야 함)

DEBUG = True  # 개발 환경에서는 True, 배포 환경에서는 False로 설정

ALLOWED_HOSTS = []  # 허용할 도메인 (배포 시 도메인 추가 필요)


# 📌 Django 애플리케이션 등록
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'youtube_api',  # ✅ 사용자 정의 앱 추가
    'naver_api',    # ✅ 새로 분리한 Naver API 앱 추가
]

# 📌 Django 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 프로젝트의 기본 URL 설정
ROOT_URLCONF = 'config.urls'

# 📌 Django 템플릿 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ✅ 템플릿 디렉토리 설정
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 애플리케이션 설정
WSGI_APPLICATION = 'config.wsgi.application'


# 📌 데이터베이스 설정 (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # ✅ PostgreSQL 데이터베이스 사용
        'NAME': 'myproject_db',  # 데이터베이스 이름
        'USER': 'myproject_user',  # 데이터베이스 사용자 이름
        'PASSWORD': 'secure_password',  # 데이터베이스 비밀번호
        'HOST': 'localhost',  # 로컬에서 실행할 경우 localhost
        'PORT': '5432',  # PostgreSQL 기본 포트
        'OPTIONS': {
            'client_encoding': 'UTF8',  # 데이터베이스 문자 인코딩 설정
        },
    }
}


# 📌 비밀번호 검증 정책 (보안 강화)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 📌 언어 및 시간대 설정
LANGUAGE_CODE = 'ko-kr'  # 한국어 설정

TIME_ZONE = 'UTC'  # 기본 시간대 (배포 시 한국 표준시 "Asia/Seoul"로 변경 가능)

USE_I18N = True  # 국제화 지원

USE_TZ = True  # 타임존 사용


# 📌 정적 파일 설정 (CSS, JavaScript, 이미지 등)
STATIC_URL = '/static/'  # 정적 파일 URL 경로

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # ✅ 개발 시 사용할 정적 파일 디렉토리
]

# ✅ 추가된 부분: 정적 파일을 한 곳에 모아 배포할 디렉토리 설정
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # `collectstatic` 명령어 실행 시 사용됨


# 기본 자동 증가 키 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

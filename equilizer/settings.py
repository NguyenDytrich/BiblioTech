***REMOVED***
Django settings for equilizer project.

***REMOVED***

***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***

***REMOVED***
***REMOVED***


***REMOVED***
***REMOVED***

***REMOVED***
SECRET_KEY = '34epm4=co#p=n%yqir#5lrsq@8%h8b^(ndsdidj2jqs6--n3er'

***REMOVED***
***REMOVED***

***REMOVED***


***REMOVED***

***REMOVED***
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
***REMOVED***

***REMOVED***
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
***REMOVED***

ROOT_URLCONF = 'equilizer.urls'

***REMOVED***
***REMOVED***
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [***REMOVED***,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ***REMOVED***,
***REMOVED***
***REMOVED***
***REMOVED***

WSGI_APPLICATION = 'equilizer.wsgi.application'


***REMOVED***
# ***REMOVED***#databases

***REMOVED***
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
***REMOVED***
***REMOVED***


***REMOVED***
# ***REMOVED***#auth-password-validators

***REMOVED***
***REMOVED***
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
***REMOVED***
***REMOVED***
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
***REMOVED***
***REMOVED***
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
***REMOVED***
***REMOVED***
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
***REMOVED***
***REMOVED***


***REMOVED***
***REMOVED***

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

***REMOVED***

***REMOVED***

***REMOVED***


***REMOVED***
***REMOVED***

STATIC_URL = '/static/'

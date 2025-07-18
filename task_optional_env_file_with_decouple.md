# Environment Variables with Python Decouple

# TL;DR
## Install
```bash
pip install python-decouple
```

## File Structure
```
project/
├── .env          # Environment variables (DO NOT commit)
├── .env.example  # Template (commit this)
└── .gitignore    # Add .env here
```

## .env File Location
- **Root directory** of your project (same level as `manage.py` in Django)
- Never commit `.env` to version control (because it will contain secret keys)
- Always add `.env` to `.gitignore`

## Usage in Python
```python
from decouple import config

# So easy!
VARIABLE_NAME = config('VARIABLE_NAME')
```

## .env File Format
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sk-1234567890
ALLOWED_HOSTS=localhost,127.0.0.1,.yourdomain.com
```

**Rules:**
- No spaces around `=`
- No quotes needed (decouple handles them)
- Use `True`/`False` for booleans
- Separate multiple values with commas




# Details

## Django settings.py example
```python
# settings.py
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432', cast=int),
    }
}
```

## .env.example Template
```
# Database
DB_NAME=myproject
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# External APIs
OPENAI_API_KEY=sk-your-key-here
```

## Key Benefits
- **Separation of concerns**: Code vs configuration
- **Security**: Sensitive data never in version control
- **Environment parity**: Same code, different configs
- **Type safety**: Automatic casting with validation
- **Defaults**: Graceful fallbacks for missing variables

## Production Deployment
- Copy `.env.example` to `.env`
- Fill in production values
- Ensure `.env` has proper file permissions (600)
- Never expose `.env` in logs or error messages

**Bottom line**: Decouple keeps secrets out of code. Put `.env` in project root, never commit it, always use type casting.


# Below part is OVERKILL, but it's here for reference
## Usage in Python
```python
from decouple import config, Csv

# Basic usage
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

# Type casting
PORT = config('PORT', default=8000, cast=int)
RATE_LIMIT = config('RATE_LIMIT', default=1.5, cast=float)

# CSV values
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
```

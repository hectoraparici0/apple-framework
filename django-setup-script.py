#!/usr/bin/env python3
"""
Django Project Setup Script
Creates a Django project structure with custom app integration.
Combines automated setup with comprehensive error handling.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


class DjangoProjectSetup:
    def __init__(self, project_name, app_name, base_path=None):
        """
        Initialize project setup with configuration parameters.
        
        Args:
            project_name (str): Name of the Django project
            app_name (str): Name of the app to create
            base_path (str, optional): Base directory for project. Defaults to current directory.
        """
        self.project_name = project_name
        self.app_name = app_name
        self.base_path = Path(base_path if base_path else os.getcwd())
        self.project_path = self.base_path / self.project_name
        self.app_path = self.project_path / self.app_name
        self.project_settings_path = self.project_path / self.project_name
        
        # Ensure essential directories exist
        self.base_path.mkdir(parents=True, exist_ok=True)

    def run_setup(self):
        """Execute the complete setup process"""
        steps = [
            (self.setup_environment, "Setting up Django environment"),
            (self.create_project_structure, "Creating project structure"),
            (self.create_settings_module, "Creating settings module"),
            (self.integrate_external_code, "Integrating external code"),
            (self.initialize_database, "Initializing database"),
        ]

        for step_func, step_desc in steps:
            print(f"\n→ {step_desc}...")
            if not step_func():
                print(f"\n× Setup failed during: {step_desc}")
                return False
        
        self._print_success_message()
        return True

    def setup_environment(self):
        """Install Django and verify Python environment"""
        try:
            # Try pip3 first, then pip
            for pip_cmd in ["pip3", "pip"]:
                try:
                    subprocess.run(
                        [pip_cmd, "install", "django"],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print("✓ Django installed successfully")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            print("× Failed to install Django with pip or pip3")
            return False
            
        except Exception as e:
            print(f"× Error during environment setup: {str(e)}")
            return False

    def create_project_structure(self):
        """Create the basic project structure"""
        try:
            # Create project directories
            for path in [self.project_path, self.project_settings_path, self.app_path]:
                path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__ files
            self._write_file(self.project_settings_path / '__init__.py', '')
            self._write_file(self.app_path / '__init__.py', '')
            
            # Create manage.py
            manage_py_path = self.project_path / 'manage.py'
            self._create_manage_py(manage_py_path)
            os.chmod(manage_py_path, 0o755)
            
            # Create app structure
            self._create_app_files()
            
            print("✓ Project structure created successfully")
            return True
            
        except Exception as e:
            print(f"× Error creating project structure: {str(e)}")
            return False

    def create_settings_module(self):
        """Create all necessary settings and configuration files"""
        try:
            # Create core project files
            self._create_settings_py()
            self._create_urls_py()
            self._create_wsgi_py()
            self._create_asgi_py()
            
            print("✓ Settings module created successfully")
            return True
            
        except Exception as e:
            print(f"× Error creating settings module: {str(e)}")
            return False

    def integrate_external_code(self, custom_files=None):
        """Integrate external Python files into the app"""
        try:
            if custom_files is None:
                custom_files = {
                    "apple_exploit_framework": self.base_path / "apple_exploit_framework.py",
                    "apple_framework": self.base_path / "apple_framework.py",
                }

            for source_name, source_path in custom_files.items():
                source_path = Path(source_path)
                if not source_path.exists():
                    print(f"× Warning: Source file {source_path} not found")
                    continue
                
                dest_path = self.app_path / f"{source_name}.py"
                shutil.copy2(source_path, dest_path)
                print(f"✓ Integrated {source_path.name}")
            
            return True
            
        except Exception as e:
            print(f"× Error integrating external code: {str(e)}")
            return False

    def initialize_database(self):
        """Initialize the database with migrations"""
        try:
            # Try python3 first, then python
            for python_cmd in ["python3", "python"]:
                try:
                    # Make migrations
                    subprocess.run(
                        [python_cmd, "manage.py", "makemigrations"],
                        cwd=self.project_path,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    
                    # Apply migrations
                    subprocess.run(
                        [python_cmd, "manage.py", "migrate"],
                        cwd=self.project_path,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    
                    print("✓ Database initialized successfully")
                    return True
                    
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            print("× Failed to initialize database with python or python3")
            return False
            
        except Exception as e:
            print(f"× Error initializing database: {str(e)}")
            return False

    def _create_manage_py(self, path):
        """Create the manage.py file"""
        content = f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
        self._write_file(path, content)

    def _create_app_files(self):
        """Create the basic app files"""
        # Create apps.py
        apps_content = f'''from django.apps import AppConfig

class {self.app_name.title().replace("_", "")}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{self.app_name}'
'''
        self._write_file(self.app_path / 'apps.py', apps_content)
        
        # Create other app files
        self._write_file(self.app_path / 'models.py', '"""Models for the app."""\nfrom django.db import models\n')
        self._write_file(self.app_path / 'views.py', '"""Views for the app."""\nfrom django.shortcuts import render\n')
        self._write_file(self.app_path / 'urls.py', '"""URLs for the app."""\nfrom django.urls import path\n\nurlpatterns = []\n')
        self._write_file(self.app_path / 'admin.py', '"""Admin configuration."""\nfrom django.contrib import admin\n')
        
        # Create migrations directory
        migrations_path = self.app_path / 'migrations'
        migrations_path.mkdir(exist_ok=True)
        self._write_file(migrations_path / '__init__.py', '')

    def _create_settings_py(self):
        """Create the settings.py file"""
        content = f'''"""
Django settings for {self.project_name} project.
"""
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{self.app_name}.apps.{self.app_name.title().replace("_", "")}Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{self.project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{self.project_name}.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
        self._write_file(self.project_settings_path / 'settings.py', content)

    def _create_urls_py(self):
        """Create the urls.py file"""
        content = '''"""URL configuration for the project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
'''
        self._write_file(self.project_settings_path / 'urls.py', content)

    def _create_wsgi_py(self):
        """Create the wsgi.py file"""
        content = f'''"""
WSGI config for {self.project_name} project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings')
application = get_wsgi_application()
'''
        self._write_file(self.project_settings_path / 'wsgi.py', content)

    def _create_asgi_py(self):
        """Create the asgi.py file"""
        content = f'''"""
ASGI config for {self.project_name} project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings')
application = get_asgi_application()
'''
        self._write_file(self.project_settings_path / 'asgi.py', content)

    def _print_success_message(self):
        """Print success message with next steps"""
        print("\n✓ Setup completed successfully!")
        print(f"\nYour project is ready at: {self.project_path}")
        print("\nNext steps:")
        print(f"1. cd {self.project_path}")
        print("2. python manage.py runserver")
        print("\nTo create a superuser:")
        print("python manage.py createsuperuser")

    @staticmethod
    def _write_file(path, content):
        """Helper method to write content to a file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.lstrip())


def main():
    """Main execution function"""
    base_path = os.getenv('DJANGO_PROJECT_PATH', './')
    project_name = "apple_integration_project"
    app_name = "apple_framework_integration"
    
    setup = DjangoProjectSetup(project_name, app_name, base_path)
    if not setup.run_setup():
        sys.exit(1)


if __name__ == '__main__':
    main()

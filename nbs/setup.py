#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# EDITS -------
import pathlib

THIS_FILE_PATH = pathlib.Path(__file__).resolve()
NBS_DIR = THIS_FILE_PATH.parent
REPO_DIR = NBS_DIR.parent
DJANGO_BASE_DIR = REPO_DIR / "src"


def init_django(project_name="cfehome"):
    """Run administrative tasks."""
    os.chdir(DJANGO_BASE_DIR)
    sys.path.insert(0, str(DJANGO_BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django
    django.setup()


"""
The given script is a modified version of Django's default `manage.py`, with added customizations to set up the Django environment more flexibly.

---

### Key Changes and Explanation:

1. **Set Paths Dynamically**:
   ```python
   import pathlib

   THIS_FILE_PATH = pathlib.Path(__file__).resolve()
   NBS_DIR = THIS_FILE_PATH.parent
   REPO_DIR = NBS_DIR.parent
   DJANGO_BASE_DIR = REPO_DIR / "src"
   ```
   - **Purpose**: Dynamically determines the paths for the current script (`THIS_FILE_PATH`), its directory (`NBS_DIR`), and the project repository's base directory (`REPO_DIR`).
   - **Custom Base Directory**: The `DJANGO_BASE_DIR` points to `src`, where the Django project code resides. This avoids hardcoding paths.

---

2. **Custom Initialization with `init_django`**:
   ```python
   def init_django(project_name="cfehome"):
       ""Run administrative tasks.""
       os.chdir(DJANGO_BASE_DIR)
       sys.path.insert(0, str(DJANGO_BASE_DIR))
       os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
       os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
       import django
       django.setup()
   ```
   - **Changing the Working Directory**: 
     `os.chdir(DJANGO_BASE_DIR)` ensures that the script starts execution from the `src` directory, where the Django project resides.
   - **Adding to `sys.path`**:
     `sys.path.insert(0, str(DJANGO_BASE_DIR))` ensures Python can locate the Django project and its modules.
   - **Setting Default Settings Module**:
     `os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')` specifies the Django settings module dynamically using the `project_name` parameter (default: `"cfehome"`).
   - **Allowing Unsafe Async**:
     `os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"` disables Django's safeguard against running unsafe synchronous ORM queries in asynchronous contexts.
   - **Initializing Django**:
     `django.setup()` sets up Django for use, enabling ORM operations, model imports, and other Django-related functionalities.

---

### Why Was It Changed?

This customization:
1. **Makes the Script Portable**:
   Dynamically determines paths instead of hardcoding them, so the script works regardless of where it's moved within the project.

2. **Supports Custom Project Structures**:
   By pointing to `src` and dynamically setting the `DJANGO_SETTINGS_MODULE`, the script adapts to projects with non-standard layouts.

3. **Allows Async-Safe Bypassing**:
   The `DJANGO_ALLOW_ASYNC_UNSAFE` variable bypasses errors when Django ORM is called in an async context. Useful in development/testing but should be avoided in production.

---

### Usage:
1. **Initialize Django in Other Scripts**:
   Instead of always running `manage.py`, call `init_django()` to set up the Django environment in any Python script.

   Example:
   ```python
   init_django("myproject")
   from myapp.models import MyModel

   print(MyModel.objects.all())
   ```

2. **Flexible for Multiple Projects**:
   The `project_name` parameter lets you easily switch between different Django projects without changing the script.

"""
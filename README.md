# Explore DRF

This is the backend api built with Django Rest Framework.

# Steps to follow

1. Setup virtual environment

   ```python
     python -m venv env
   ```

   or

   ```python
     python3 -m venv env
   ```

2. Install packages

   ```python
   pip install -r requirements.txt
   ```

3. Make migrations and migrate

   - If you use the provided db.sqlite3 some seed data is already insertef, delete the file db.sqlite3 and then migrate if you want to use your custom data
   - Admin credentials are:
       - Email: admin@admin.com
       - Password: admin123

4. Start server using
   ```python
   python manage.py runserver
   ```

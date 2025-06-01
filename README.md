# Kalimantan Tourism Website

A Flask-based website showcasing tourism destinations in Kalimantan, Indonesia.

## Setup Instructions for PythonAnywhere

1. Create a PythonAnywhere account if you haven't already at https://www.pythonanywhere.com

2. Set up MySQL Database:
   - Go to the Databases tab in PythonAnywhere
   - Create a new MySQL database
   - Note down your database credentials:
     - Username (your PythonAnywhere username)
     - MySQL hostname (username.mysql.pythonanywhere-services.com)
     - Password (the one you set)
     - Database name (username$kalimantan_tourism)

3. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd kalimantan_tourism
   ```

4. Create and activate a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 kalimantan_env
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Create `.env` file:
   - Copy `.env.example` to `.env`
   - Update the database credentials with your PythonAnywhere MySQL credentials
   - Update the secret key

7. Configure Web App in PythonAnywhere:
   - Go to the Web tab
   - Add a new web app
   - Choose Manual Configuration
   - Choose Python 3.9
   - Set the following paths:
     - Source code: /home/rjscrapy/kalimantan_tourism
     - Working directory: /home/rjscrapy/kalimantan_tourism
     - Virtual environment: /home/rjscrapy/.virtualenvs/kalimantan_env

8. Configure WSGI File:
   - Click on the WSGI configuration file link
   - Replace the content with:
   ```python
   import sys
   import os
   from dotenv import load_dotenv

   path = '/home/rjscrapy/kalimantan_tourism'
   if path not in sys.path:
       sys.path.append(path)

   load_dotenv(os.path.join(path, '.env'))

   from app import app as application
   ```

9. Initialize Database:
   - Open a PythonAnywhere console
   - Navigate to your project directory
   - Run Python console:
   ```python
   from app import app, init_db
   with app.app_context():
       init_db()
   ```

10. Reload your web app from the Web tab

Your website should now be live at rjscrapy.pythonanywhere.com

## Local Development

1. Create a MySQL database locally:
   ```sql
   CREATE DATABASE kalimantan_tourism;
   ```

2. Copy `.env.example` to `.env` and update with local database credentials:
   ```
   DATABASE_URL=mysql+pymysql://username:password@localhost/kalimantan_tourism
   SECRET_KEY=your-secret-key-here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The site will be available at http://localhost:5000

## Features
- Dynamic destination listings
- Detailed destination pages
- MySQL database integration
- Environment-based configuration
- Developer profile page

## Database Schema

### Destinations Table
- id (Primary Key)
- name (String, Unique)
- location (String)
- description (Text)
- image (String)
- created_at (DateTime)
- updated_at (DateTime)

# How to run
(*Optional) change `.env` file before 
## Python
Create .venv: `python -m venv .venv`  
Install dependencies: `pip install -r requirements.txt`  
Run database: `docker-compose up -d db`  
Migrate: `python manage.py migrate`  
Run server: `python manage.py runserver`
## Docker
Run Docker and execute: `docker-compose up --build`

# Implemention
1. **Main endpoints**  
You can get weather by city: `/weather?city=[city]`  
Query params:
- city - interesting city for get weather.
- unit (optional, default=C) - set temperature measure units (C - Celsius , F - Fahrenheits).

You can get requests history: `/weather/history/`  
Query params:
- city (optional) - filter history by city.
- to (optional) - filter history by start date.
- from (optional) - filter history by end date.
- export (optional) - set 'CSV' for csv export

For get database health info: `/health/`

2. **Cache**
The application uses caching, which reduces the load on the server and
eliminates the possibility of duplicates.
3. **Throttling**
The application has a limited request rate to prevent DDoS attacks.
4. **CSV export**
Application provides CSV export.
5. Application has tests. For run: `pytest`
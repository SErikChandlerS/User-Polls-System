# User Polls System

## How to up backend 

```
cd DRF-Poll-Test
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
```
Creating superuser with login - admin, and password - admin
This user will be used in unit-tests (tests/settings.py).

### Up server
```
cd DRF-Poll-Test/backend
python manage.py runserver
```

### Launch polls
Tests should be launched when server is up 
```
cd DRF-Poll-Test/tests
pytest
```

## API description

[API.md](API.md)


## Database scheme

![schema](schema.svg)

# User Polls System
## Detailed project information
![Detailed information of project.](https://docs.google.com/document/d/1A799J1TsTdoqfzb9RM6FuLdGwPA2g4mxi-ezcD3aFW0/edit?usp=sharing) It includes information about stakeholders, user stories and other requirements.
## Getting Started

```
cd DRF-Poll-Test
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
```
Creating superuser with login - admin, and password - admin
This user will be used in unit-tests (tests/settings.py).

### Setup server
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

FLASK_ENV=development
FLASK_APP=login.app:create_app
SECRET_KEY=changeme
DATABASE_URI=sqlite:////tmp/login.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/

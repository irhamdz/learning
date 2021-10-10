# flask-send-mail

Web app for sending mail based on timestamp given build with flask

## Development

- Create and activate new Python virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

- Install dependencies

```bash
pip install -r requirements.txt
```

- Set env variables for local machine

```bash
export FLASK_APP=flask_send_mail
export FLASK_ENV=development
```

- Initialize database

```bash
flask init-db
```

- Run app

```bash
flask run
```

- Testing

```bash
# make sure you install the application first
pip install -e .

# if db not found
flask init-db

# run tests
pytest
```

### Using Scheduler

- install rabbitMQ on your local machine , for detail step of installation you can go to
this [link](https://docs.celeryproject.org/en/stable/getting-started/brokers/rabbitmq.html#installing-the-rabbitmq-server)

- create your mailtrap account, sign up or create through this [link](https://mailtrap.io/register/signup)

- set env for mailtrap user and pass
```bash
export MAIL_USERNAME='your-mailtrap-username'
export MAIL_PASSWORD='your-mailtrap-password'
```

- run celery command

```bash
celery -A flask_send_mail.tasks.celery worker -l info -B
```

## API SPEC

please go to this [link](API_SPEC.md) to see the api spec for available endpoints.
# goit-pythonweb-hw-12

For local running make sure you have:

- [Docker Engine](https://docs.docker.com/engine/install/) installed first
- email account on [META.ua](https://meta.ua/uk/) (or any other mail server for email sending)
- account on [Cloudinary](https://cloudinary.com/)

In the root directory create `.env` file with next content:

```
POSTGRES_DB=<db_name>
POSTGRES_USER=<db_user_name>
POSTGRES_PASSWORD=<db_user_password>
POSTGRES_PORT=5432
POSTGRES_HOST=postgress (name of the postgress service container)

MAIL_USERNAME=<your_email>@meta.ua
MAIL_PASSWORD=<email_password>
MAIL_FROM=<your_email>@meta.ua
MAIL_PORT=465
MAIL_SERVER=smtp.meta.ua

CLD_NAME=<your_cloudinari_name>
CLD_API_KEY=<your_cloudinari_api_key>
CLD_API_SECRET=<your_cloudinari_api_secret>

DB_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
JWT_SECRET=<your_secret_key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
```

### Run

Execute the command to build and start the application

```bash
docker-compose up --build
```

Click the [link](http://127.0.0.1:8000/docs) to open API documentation

### Tests

Run pytests and generate the test coverage report

```bash
pytest --cov=src tests/ --cov-report=html
```

Check tests coverage HTML
[link](htmlcov/index.html)

Check the doc file HTML
[link](docs/_build/html/index.html)
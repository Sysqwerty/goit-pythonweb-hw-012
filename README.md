# goit-pythonweb-hw-10



Make sure you have:
- [Docker Engine](https://docs.docker.com/engine/install/) installed first
- email account on [META.ua](https://meta.ua/uk/) (for email sending)
- account on [Cloudinary](https://cloudinary.com/)

In the root directory create `.env` file with next content:
```
POSTGRES_DB=<db_name>
POSTGRES_USER=<db_user_name>
POSTGRES_PASSWORD=<db_user_password>
POSTGRES_PORT=5432
POSTGRES_HOST=localhost

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

```bash
poetry shell
```

```bash
poetry install
```

```bash
docker-compose up -d
```

```bash
alembic upgrade head
```

```bash
fastapi dev main.py
```

Open in browser SWAGGER doc: [link](http://127.0.0.1:8000/docs#/)
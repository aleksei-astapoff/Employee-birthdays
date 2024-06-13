FROM python:3.11
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install gunicorn==20.1.0
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN mkdir -p /app/sent_emails && chmod -R 777 /app/sent_emails
RUN python manage.py makemigrations
RUN python manage.py collectstatic --noinput
RUN groupadd -r celery && useradd -r -g celery celery
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "emploe_birthdays.wsgi"]

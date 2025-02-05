FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libicu-dev \
    icu-devtools \
    locales \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgdiplus \
    libssl-dev \
    && apt-get clean

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

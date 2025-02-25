FROM python:3.11

WORKDIR /app

# Устанавливаем libssl1.1 и создаем симлинки, если нужно
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libgdiplus \
    libssl1.1 \
    && ln -sf /usr/lib/x86_64-linux-gnu/libssl.so.1.1 /usr/lib/x86_64-linux-gnu/libssl.so \
    && ln -sf /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 /usr/lib/x86_64-linux-gnu/libcrypto.so \
    && ldconfig \
    && apt-get clean

# Указываем, что libssl1.1 должен быть в пути поиска библиотек
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

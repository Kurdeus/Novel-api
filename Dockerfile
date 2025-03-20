FROM python:3.10

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "7860"]

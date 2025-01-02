FROM python:3.12

WORKDIR /app/backend

COPY ./src/backend/requirements.txt /app/backend

RUN pip install --no-cache-dir -r requirements.txt

# サーバー起動コマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8083
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0:8083", "main:app" ]

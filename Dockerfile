FROM python:3.12
# EXPOSE 5000 # Using gunicorn, so no need to expose port
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
FROM python:3.10
EXPOSE 5000
WORKDIR /app
# Copiamos el requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask","run","--host","0.0.0.0"]
# Build -> docker build -t "message: flask-smorest-api" .
# Run Docker -> docker run -dp 5000:5000 flask-smorest-api
# Para actualizar el app.py -> docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api
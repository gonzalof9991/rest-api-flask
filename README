# Curso RestApi Flask

- Es un buen curso para aprender las bases de Flask, en el trayecto del curso

## Librerias

### passlib:

- Permite hacer hash de nuestras contraseñas o hacerlas ilegibles cuando las pongamos en nuestra base de datos.
- De este modo si alguien consigue acceder a nuestra base de datos, no podrá ver las contraseñas almacenadas en texto
  plano.

## Notas

### Agregar Flask-Migrate Alembic a Flask app
- Paso 1:
  - Activar entorno virtual
  - pip install flask-migrate
  - lo añadimos a requirements.txt
  - Importar Migrate en app.py
  - Inicializar variable migrate = Migrate(app,db)
- Paso 2 (Inicializar BD):
  - flask db init
  - Eliminar db o carpeta instance
  - flask db migrate
  - flask db upgrade
- Importante:
    - Cada vez que se modifique un Modelo, etc,  se debe correr el comando flask db migrate
    - Posterior a eso para actualizar la BD el comando seria flask db upgrade

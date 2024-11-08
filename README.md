The PROJECT covers a online uniform store based on flask.

Files in the app include :

STATIC FILES(includes css,html templates, javascript and images used)

INIT FILE

FORMS, MODELS(databse tables)

VIEWS file(or the routes page)

REQUIREMENTS FILES(contains file dependencies)

and a RUN.PY file for firing up the app

Codes to run the app.

python run.py or python3 run.py

using a wsgi server such as gunicorn with nginx : gunicorn -w 4 -b 0.0.0.8000 run:app

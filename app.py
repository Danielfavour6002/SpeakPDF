from flask import Flask
import os
from core import create_app, make_celery


app, celery = create_app()

if __name__ == '__main__':
    app.run(debug=True)




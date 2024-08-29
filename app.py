from flask import Flask
import os
from core import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)




from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

from views import *

if __name__ == "__main__":
    app.run(debug=True)

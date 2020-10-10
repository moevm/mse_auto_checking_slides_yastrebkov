from flask import Flask
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

bootstrap = Bootstrap(app)

from views import *

dir = os.getcwd()

conf = open(dir + '\\config.txt', 'w')
conf.write(dir)
conf.close()

if __name__ == "__main__":
    app.run(debug=True)

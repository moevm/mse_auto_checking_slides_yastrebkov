import sys
from flask import Flask
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

bootstrap = Bootstrap(app)

from views import *

directory = os.getcwd()
print(directory)

conf = open(os.path.join(directory, 'config.txt'), 'w')
conf.write(directory)
conf.close()

host = "0.0.0.0"
port = "80"

if len(sys.argv) == 5:
    try:
        host_idx = sys.argv.index('--host')
        port_idx = sys.argv.index('--port')
        host = sys.argv[host_idx + 1]
        port = sys.argv[port_idx + 1]
    except ValueError:
        pass

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)

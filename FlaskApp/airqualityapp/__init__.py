from flask import Flask

app = Flask(__name__)

from airqualityapp import routes

from flask import Flask

app = Flask(__name__)

from book_app import routes

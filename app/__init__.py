from flask import Flask

app = Flask(__name__)
app.secret_key = '8f42a73054b1749f8f58848be5e6502c'
from app import routes
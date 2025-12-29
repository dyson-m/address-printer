from flask import Flask
import base64

app = Flask(__name__)
app.secret_key = '8f42a73054b1749f8f58848be5e6502c'

@app.template_filter("b64_encode")
def b64encode_filter(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")

from app import routes
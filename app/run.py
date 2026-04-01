from flask import Flask
from app.db.schema import create_schema

app = Flask(__name__)
create_schema()

@app.route("/")
def lancamentos():
    return "Hell"

if __name__ == '__main__':
    app.run(debug=True)

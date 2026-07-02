from app import create_app
from app.config import DEBUG
from app.scripts.schema import create_schema

# Explicit runtime setup: initialize the schema before serving requests.
create_schema()
app = create_app()

if __name__ == '__main__':
    app.run(debug=DEBUG)

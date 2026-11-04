from app import create_app
from app.scripts.schema import create_schema

app = create_app()


def main():
    with app.app_context():
        create_schema()
    app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    main()

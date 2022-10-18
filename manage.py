# manage.py
from project.server import create_app
from flask_cors import CORS

# code coverage
app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run()

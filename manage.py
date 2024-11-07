import sys
sys.path.insert(0, '/Users/zulfikarshariff/Desktop/Programs/Educational')
from flask import Flask
from flask_migrate import Migrate
from selidiq import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(port=5001)


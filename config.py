import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": os.path.join(os.path.dirname(__file__), "ca.pem")
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
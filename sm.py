
from flask_sqlalchemy import SQLAlchemy
import dash
from pathlib import Path

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_URL = f"sqlite:///{Path(__file__).parent}/exchange.db"
app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)
server = app.server
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
server.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(server)
# time = db.session.query(Cu)

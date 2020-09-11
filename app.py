import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import dash
import dash_core_components as dcc
import dash_html_components as html


# app = Flask(__name__)
#
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
# app.config["SECRET_KEY"] = "hard to guess string"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "data.sqlite"
# )
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# db = SQLAlchemy(app)
#
#
# class Role(db.Model):
#     __tablename__ = "roles"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship("User", backref="role", lazy="dynamic")
#
#     def __repr__(self):
#         return "<Role %r>" % self.name
#
#
# @app.route('/')
# def hello_world():
#     return render_template('index.html') #this has changedprint(path.parent.parent)
#
#
# if __name__ == '__main__':
#     app.run()


# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {"background": "#111111", "text": "#7FDBFF"}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.plot(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
)

markdown_text = """
Данные о курсах взяты отсюда(https://www.bestchange.net)
"""

# app.layout = html.Div([
#     dcc.Markdown(children=markdown_text)
# ])

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Анализ обменников на базе платформы BestChange",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Graph(id="example-graph-2", figure=fig),
        dcc.Markdown(
            markdown_text, style={"textAlign": "center", "color": colors["text"]}
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)

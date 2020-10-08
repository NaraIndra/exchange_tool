import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path
from data_processing.data_processing import (
    # update_data,
    pair_find_leader,
    find_cp_leaderpoints_minutes,
    find_cp_last_datetime,
)
from data_processing.db_processing import update_data
from db.db_model import db, Currency, Saler, Currency_pair
from globals import (
    minute2_datetime_label_g,
    minute10_datetime_label_g,
    hour_datetime_label_g,
    day_datetime_label_g,
)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {"background": "#111111", "text": "#7FDBFF"}

c_give_num = 29
c_take_num = 139

session = db.session

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_data, args=[db.session, sched], trigger="interval", minutes=2)
sched.start()
# обработка датки
# update_data()
last_date = find_cp_last_datetime(c_give_num, c_take_num)
leader = pair_find_leader(
    currency_give_num=c_give_num, currency_take_num=c_take_num, last_datetime=last_date
)
points = find_cp_leaderpoints_minutes(
    leader_num=leader,
    last_datetime=last_date,
    currency_give=c_give_num,
    currency_take=c_take_num,
)

# отрисовка датки
if not points.empty:
    fig = px.line(x=points["datetime"], y=points["amount_give"])
    # title=f'продажа {cur_give_name}\n покупка {cur_take_name}')

fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
)

markdown_text = """
Данные о курсах взяты c сайта https://www.bestchange.net
"""


app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Анализ обменников на базе платформы BestChange",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Markdown(
            markdown_text, style={"textAlign": "center", "color": colors["text"]}
        ),
        dcc.Graph(id="graph_with_slider", figure=fig),
        dcc.Slider(
            id="time-slider",
            min=1,
            max=7,
            value=1,
            marks={
                str(i): name
                for i, name in zip(
                    range(2, 7), ["2 минуты", "10 минут", "час", "день", "неделя"]
                )
            },
            step=None,
        ),
    ],
)


# @app.callback(Output("graph-with-slider", "figure"), [Input("year-slider", "value")])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#
#     fig = px.scatter(
#         filtered_df,
#         x="gdpPercap",
#         y="lifeExp",
#         size="pop",
#         color="continent",
#         hover_name="country",
#         log_x=True,
#         size_max=55,
#     )

# fig.update_layout(transition_duration=500)
#
# return fig


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)

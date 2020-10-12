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
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
from data_processing.data_processing import (
    # update_data,
    pair_find_leader,
    find_cp_leaderpoints_minutes,
    find_cp_last_datetime,
)
from sm import app, db
from data_processing.db_processing import update_data
from db.db_model import Currency, Saler, Currency_pair
from globals import (
    minute2_datetime_label_g,
    minute10_datetime_label_g,
    hour_datetime_label_g,
    day_datetime_label_g,
)


colors = {"background": "#111111", "text": "#7FDBFF"}

c_give_num = 29
c_take_num = 139

session = db.session

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_data, args=[db.session, sched], trigger="interval", minutes=2)
sched.start()

c_give_num = 29
c_take_num = 139
fig = None


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
        dcc.Dropdown(id="give_currency_dropdown",
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        placeholder="Выберите отдаваемую валюту",
        ),
        dcc.Dropdown(id="take_currency_dropdown",
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            placeholder="Выберите получаемую валюту",
        ),
        dcc.Graph(id="live_update_graph"),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000 * 50, # в милисекундах
            n_intervals=0
        )
        # dcc.Slider(
        #
        # )
    ],
)

@app.callback(
    Output(component_id='live_update_graph', component_property='figure'),
    [Input('interval-component', 'n_intervals')])
def update_plot(n):
    c_give_num = 29
    c_take_num = 139
    fig = None
    last_date = find_cp_last_datetime(c_give_num, c_take_num)
    leader = pair_find_leader(
        currency_give_num=c_give_num, currency_take_num=c_take_num, last_datetime=last_date
    )
    print('leader ', leader)
    points = find_cp_leaderpoints_minutes(
        leader_num=leader,
        last_datetime=last_date,
        currency_give=c_give_num,
        currency_take=c_take_num,
    )
    print('points ', points['datetime'], points['amount_give'])
    if points.empty:
        return None
    fig = px.line(x=points["datetime"], y=points["amount_give"])
    # fig.add_trace(go.line(x=points["datetime"], y=points["amount_take"]))
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)

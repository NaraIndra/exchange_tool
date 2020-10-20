import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data_processing.data_processing import (
    pair_find_leader,
    find_cp_leaderpoints_minutes,
    find_cp_last_datetime,
)
from db.db_model import Currency
from sm import app, db
from data_processing.db_processing import update_data_pandas
from dash.exceptions import PreventUpdate


session = db.session

colors = {"background": "#111111", "text": "#7FDBFF"}

# currency_data = pd.read_csv('../datadir/bm_cy.csv', )

data = pd.read_sql(
    db.session.query(Currency.num, Currency.name)
        .statement,
    db.session.bind
)
options = [{"label": x[1], "value": x[0]} for x in data.values]


sched = BackgroundScheduler(daemon=True)
#sched.add_job(update_data, args=[db.session, sched], trigger="interval", minutes=2)
sched.add_job(update_data_1, args=[sched], trigger="interval", minutes=2)
sched.start()

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
        html.Label(["Выберите отдаваемую валюту", dcc.Dropdown(id="give_currency_dropdown_dynamic",
        placeholder="список валют")]),
        html.Label(["Выберите получаемую валюту", dcc.Dropdown(id="take_currency_dropdown_dynamic",
        placeholder = "список валют")]),
        dcc.Graph(id="live_update_graph"),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000 * 50, # в милисекундах
            n_intervals=0
        )
    ],
)
@app.callback(
    dash.dependencies.Output("give_currency_dropdown_dynamic", "options"),
    [dash.dependencies.Input("give_currency_dropdown_dynamic", "search_value")],
)
def update_options(search_value):
    # if not search_value:
    #     raise PreventUpdate
    if not search_value:
        return options
    return [o for o in options if search_value in o["label"]]


@app.callback(
    dash.dependencies.Output("take_currency_dropdown_dynamic", "options"),
    [dash.dependencies.Input("take_currency_dropdown_dynamic", "search_value")],
)
def update_options(search_value):
    if not search_value:
        return options
    return [o for o in options if search_value in o["label"]]

@app.callback(
    Output(component_id='live_update_graph', component_property='figure'),
    [Input('interval-component', 'n_intervals')])
def update_plot(n):
    c_give_num = 29
    c_take_num = 139
    fig = None
    #last_date = find_cp_last_datetime(c_give_num, c_take_num)
    leader = pair_find_leader_pandas(
        currency_give_num=c_give_num, currency_take_num=c_take_num, last_datetime=last_date
    )
    print('leader ', leader)
    points = find_cp_leaderpoints_minutes_pandas(
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

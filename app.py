import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path
from data_processing.data_processing import currency_find_leader_sec_points
from db.db_model import db, Currency, Saler, Currency_pair



external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {"background": "#111111", "text": "#7FDBFF"}

sec_csv = Path(__file__).parent / 'data_processing' / 'sec.csv'
# print(sec_csv)

# df = pd.read_csv(sec_csv)
# cur_df = pd.read_csv('id_currency.csv', sep=';',names=['id', 'name'])
# print(cur_df)

cur_give = 25

cur_take = 139
cur_df = pd.read_sql(db.session.query(Currency_pair).filter(Currency_pair.cur_give_num == cur_give,
          Currency_pair.cur_take_num == cur_take).statement,db.session.bind)
print(cur_df)
print(len(cur_df))
exit(-1)


leader, points = currency_find_leader_sec_points(cur_give, cur_take)

data = df.loc[df['saler_id'] == leader]

name_give = cur_df.loc[cur_df['id'] == cur_give, 'name']
name_take = cur_df.loc[cur_df['id'] == cur_take, 'name']
fig = px.line(data, x=points['datetime'], y=points['cur_give_num'], title=f'продажа {name_give.values}\n покупка {name_take.values}')


# fig = px.bar(df, x="Fruit", y="Amount")

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
            id='time-slider',
            min=1,
            max=7,
            value=1,
            marks={str(i):name  for i, name in zip(range(2,7),['секунды', 'десятки сек', 'минуты', 'часы', 'дни'])},
            step=None
        )
    ],
)

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     size="pop", color="continent", hover_name="country", 
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

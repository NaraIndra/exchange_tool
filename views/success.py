import warnings
# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app

warnings.filterwarnings("ignore")

"""
# Create success layout
layout = html.Div(children=[
    dcc.Location(id='url_login_success', refresh=True),
    html.Div(
        className="container",
        children=[
            html.Div(
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="ten columns",
                            children=[
                                html.Br(),
                                html.Div('Login successfull'),
                            ]
                        ),
                        html.Div(
                            className="two columns",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0)
                            ]
                        )
                    ]
                )
            )
        ]
    )
])


# Create callbacks
@app.callback(Output('url_login_success', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

"""
# from server import colors
colors = {"background": "#111111", "text": "#7FDBFF"}

markdown_text = """
Данные о курсах взяты c сайта https://www.bestchange.net
"""


layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Анализ обменников на базе платформы BestChange",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Markdown(
            markdown_text, style={"textAlign": "center", "color": colors["text"]}
        ),
        """
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
        """
    ],
)

# Create callbacks
@app.callback(Output('url_login_success', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

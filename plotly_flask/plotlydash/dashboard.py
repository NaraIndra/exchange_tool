from dash import Dash
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html



def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div(id='dash-container')

    return dash_app.server


# import dash
# from dash.dependencies import Input, Output
# import dash_table
# import dash_html_components as html

# def init_dashboard(server):
#     app = dash.Dash(__name__)
#     app.layout = html.Div([
#         # ... Layout stuff
#     ])

#     # Initialize callbacks after our app is loaded
#     # Pass dash_app as a parameter
#     init_callbacks(dash_app)

#     return dash_app.server

# def init_callbacks(dash_app):
#     @app.callback(
#     # Callback input/output
#     ....
#     )
#     def update_graph(rows):
#         # Callback logic
#         ...
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


dataframe = pd.DataFrame(np.random.randn(50, 26),
                         columns=['Column ' + i
                                  for i in ['A', 'B', 'C', 'D', 'E', 'F',
                                            'G', 'H', 'I', 'J', 'K', 'L',
                                            'M', 'N', 'O', 'P', 'Q', 'R',
                                            'S', 'T', 'U', 'V', 'W', 'X',
                                            'Y', 'Z']])

dataframe['Fruit'] = np.random.choice(['Apple', 'Pear', 'Grape'], 50)

trace = go.Heatmap(
    z=dataframe.corr().as_matrix(),
    x=dataframe.corr().columns,
    y=dataframe.corr().columns
)

heatmap = go.Figure(data=[trace])


def create_scatter(x, y):
    data = []
    for fruit in ['Apple', 'Pear', 'Grape']:
        data.append(
            go.Scatter(
                x=dataframe.loc[dataframe['Fruit'] == fruit, x],
                y=dataframe.loc[dataframe['Fruit'] == fruit, y],
                mode='markers',
                name=fruit
            )
        )
    return go.Figure(data=data)


app.layout = html.Div([
    dcc.Graph(id='heatmap', figure=heatmap),
    dcc.Graph(id='scatter')
])


@app.callback(
    Output('scatter', 'figure'),
    [Input('heatmap', 'hoverData')]
)
def makeScatter(hoverData):
    return create_scatter(hoverData['points'][0]['x'], hoverData['points'][0]['y'])


if __name__ == '__main__':
    app.run_server(debug=True)

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd

app = Dash(__name__)


app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-data-upload')
])

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(content, name, date):
    if content is not None:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return html.Div([
                html.H5(f'File: {name}'),
                html.P(f'Rows: {len(df)}'),
                html.P(f'Columns: {", ".join(df.columns)}')
            ])
        except Exception as e:
            return html.Div([
                'There was an error processing this file.'
            ])
    return html.Div('No file uploaded yet.')

if __name__ == '__main__':
    app.run_server(debug=True)
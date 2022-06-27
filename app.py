import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
 
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.P("Stock Visualizer and Prediction", className="start"),
        html.P('Input stock code:',className="heading"),
        html.Div(children=[
            dcc.Input(id='input-on-submit',type='text',value="Type Here", className="input"),
            html.Button('Submit', id='submit-val', n_clicks=0, className="Button"),
        ],className="code"),
        html.Div(children=[            
             dcc.DatePickerRange(
                id='date-picker-range',
                initial_visible_month=date.today(),
                start_date_placeholder_text='Start Date',
                end_date=date.today(),
                display_format='DD/MM/YYYY',
            )
        ],className="date_picker"),
        html.Div([
            html.Button(['Stock price'], id="button-1", className='Button'),
            html.Button(['Indicators'], id="button-2", className='Button'),
            #dcc.Input(id='input-val', value='Number of Days', type='text',className="input"),
            #html.Button(['Forecast'], id="button-3", n_clicks='0' , className='Button'),
        ],className="forecast"),
    ],
    className="nav"),
    html.Div(
    [
        html.Div([
            html.Img(id="img",src=" "),
            html.Div(children=[],id="head",className="header"),
        ]),
        html.Div(children=[], id="description", className="decription_ticker"),
        dcc.Graph(id="graphs-content"),
        dcc.Graph(id="main-content"),
        #dcc.Graph (id="forecast-content"),
    ],
    className="content")
],className="container")

@app.callback([
    Output("img","src"),
    Output("head", "children"),
    Output("description","children"),
    ],
    [Input('submit-val', 'n_clicks')],
    [State('input-on-submit', 'value')]
)
def update_output(n_clicks,val):
    global store
    store=val
    if n_clicks is None:
        raise PreventUpdate
    else:
        ticker = yf.Ticker(val)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient="index").T
        li=[df["logo_url"][0]]
        li.append(df["longName"][0])
        li.append(df["longBusinessSummary"][0])
        return li

@app.callback(Output("img", 'style'), [Input('submit-val','n_clicks')])
def hide_image(n_clicks):
    if n_clicks is not None:
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(
    Output("graphs-content", "figure"),  
    [Input('date-picker-range','start_date')],
    [Input('date-picker-range','end_date')],
    [Input('button-1','n_clicks')],
)
def update_output(start_date,end_date,n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = yf.download(store, start_date, end_date)
        df.reset_index(inplace=True)
        fig = get_stock_price_fig(df)
        return fig
def get_stock_price_fig(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],),
    ])
    fig.update_layout(
    title={
        'text': "Candlestick Chart",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Date",
    yaxis_title="Price")
    return fig

@app.callback(Output('graphs-content', 'style'), [Input('button-1','n_clicks')])
def hide_graph(n_clicks):
    if n_clicks is not None:
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(
    Output("main-content","figure"),
    [Input('date-picker-range','start_date')],
    [Input('date-picker-range','end_date')],
    [Input('button-2','n_clicks')],
)
def modif(start_date,end_date,n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = yf.download(store,start_date,end_date)
        df.reset_index(inplace=True)
        fig = get_more(df)
        return fig
def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
    x= "Date",
    y= "EWA_20",
    title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines')
    return fig

@app.callback(Output('main-content', 'style'), [Input('button-2','n_clicks')])
def hide_graph(n_clicks):
    if n_clicks is not None:
        return {'display':'block'}
    else:
        return {'display':'none'}

if __name__ == '__main__':
    app.run_server(debug=True)

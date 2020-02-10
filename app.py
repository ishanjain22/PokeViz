import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

#Style Sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ , external_stylesheets = external_stylesheets)

#Read CSV
df = pd.read_csv('pokemon/pokemon_alopez247.csv')
print(df.columns)

#Drop down for second graph
option_list = ["Attack", "Defense", "Speed", "Catch_Rate"]
pokemon_names = ["Bulbasaur", "Ivysaur" , "Venusaur"]

#App Layout
app.layout = html.Div(children=[
    html.H1(children = "PokeDex"),
    html.H3(children= "Similar Pokemons"),
    html.Div([
        dcc.Dropdown(
            id='option_dropdown',
            options=[
                {'label': i, 'value': i} for i in option_list
            ],
            value=["Attack"]
        )
    ],
        style={
            "width": '50%',
            'display': 'inline-block',
            'paddingLeft': 10,
            'paddingRight': 60,
            'boxSizing': 'border-box',
        }
    ),
        dcc.Checklist(
            id='pokemonCheck',
            options=[
                {'label': i, 'value': i} for i in pokemon_names
            ],
            value=[],
            labelStyle={  # Different padding for the checklist elements
                'display': 'inline-block',
                'paddingRight': 10,
                'paddingLeft': 10,
                'paddingBottom': 5,
            },

        ),
    html.Div(
        id = 'output-graph'
    ),

    html.Div([
        dcc.Graph(
            id='radar-graph'
        )
    ],
    style={
        'width' : '100%',
        'display' : 'inline-block',
        'paddingRight': 50,
        'paddingLeft': 5,
        'boxSizing' : 'border-box',
        'fontFamily' : "Arial"
    }
    )

])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='option_dropdown', component_property='value'),
     Input(component_id='pokemonCheck', component_property='value')]
)

def update_graph(option, pokemon_names):
    #Get Pokemon Names and their values corresponding to options (ex . Attack, Defense, Speed, Catch_Rate)

    option_value = []

    #Get the values for each pokemon according to selected option
    filtered_df = df[["Name","Attack", "Defense", "Speed", "Catch_Rate"]]

    for name in pokemon_names:
        option_df = df[(df.Name == name)]
        option_value.append(int(option_df.iloc[0][option]))

    print(option_value)


    return dcc.Graph(
        id='similarPokemonGraph',
        figure={
            'data': [
                {'x': pokemon_names, 'y': option_value,
                 'type': 'bar',
                 'marker': {
                     'color': '#0277bd'
                 }
                 }
            ],
            'layout': {
                'title': 'Similar Pokemons',
                'hovermode': 'closest',
                'paper_bgcolor': '#e1f5fe',
                'plot_bgcolor': '#e1f5fe',
                'height': 500,

            },

        }
    )

@app.callback(
    Output(component_id='radar-graph', component_property='figure'),
    [Input(component_id='pokemonCheck', component_property='value')]
)

def updateRadarGraph(names):
    categories = ['Attack', 'Defense', 'Sp_Atk',
                  'Sp_Def', 'Speed']

    fig = go.Figure()

    num = len(names)

    for i in range(num):
        option_df = df[(df.Name == names[i])]
        option_value = []
        for j in range(5):
            option_value.append(int(option_df.iloc[0][categories[j]]))

        fig.add_trace(go.Scatterpolar(
            r = option_value,
            theta= categories,
            fill='toself',
            name= names[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 200]
            )),
        showlegend=True,
        paper_bgcolor = '#ffffff',
        plot_bgcolor='#ffffff'

    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

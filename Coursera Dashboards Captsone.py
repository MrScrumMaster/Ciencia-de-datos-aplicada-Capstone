import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Inicializar la aplicación Dash
app = Dash(__name__)

# Cargar los datos
spacex_df = pd.read_csv('datasets/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Diseño del dashboard
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown para sitios de lanzamiento
    html.Div([
        html.Label('Select Launch Site:'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
        )
    ]),

    # Gráfico circular de éxito
    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),

    # TASK 3: Slider para rango de carga útil
    html.Div([
        html.Label('Payload Range (kg):'),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={i: str(i) for i in range(0, 10001, 1000)}
        )
    ]),

    # Gráfico de dispersión de carga útil vs éxito
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])


# TASK 2: Callback para el gráfico circular
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Datos para todos los sitios
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site'
        )
    else:
        # Datos filtrados para el sitio seleccionado
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failed Launches for site {entered_site}',
            color_discrete_map={0: 'red', 1: 'green'}
        )
    return fig


# TASK 4: Callback para el gráfico de dispersión
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites',
            labels={'class': 'Launch Outcome (0=Failed, 1=Success)'}
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {entered_site}',
            labels={'class': 'Launch Outcome (0=Failed, 1=Success)'}
        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
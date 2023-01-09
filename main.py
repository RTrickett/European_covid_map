import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output

load_figure_template("darkly")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Import and clean third vaccination uptake by % data
# df = pd.read_csv("vaccination-data.csv", usecols=['ISO3', 'COUNTRY', 'DATE_UPDATED', 'PERSONS_FULLY_VACCINATED_PER100'])
df = pd.read_csv("Covid-Poverty_data.csv")
print(df[0:5])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

# Plotly Express
fig = px.choropleth(
    data_frame=df,
    locations='ISO3',
    color='Persons_fully_vaccinated_per100',
    hover_name='Country',
    hover_data=['Persons_fully_vaccinated_per100', 'Deaths_per_million', 'Population_below_poverty_line',
                'GDP_per_capita'],
    labels={'Persons_fully_vaccinated_per100': 'Fully Vaccinated (%)',
            'Deaths_per_million': 'Covid deaths (per million)',
            'Population_below_poverty_line': 'Population Below Poverty Line (%)',
            'GDP_per_capita': 'GDP per Capita'},
)

fig.update_layout(
    #title_text="Persons Fully Vaccinated by Country (%)",
    title_xanchor="center",
    title_font=dict(size=22),
    title_x=0.5,
    margin=dict(t=5, r=0, l=0, b=5),  # remove margins
    dragmode=False,
    geo=dict(scope='europe')  # what section of the world is being shown
)

fig.update_coloraxes(showscale=True, colorbar_orientation='h')
#fig.update_layout(template='plotly_dark')
fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), coloraxis_colorbar_y=0, coloraxis_colorbar=dict(titleside='top'))  # remove background


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

fig2 = px.scatter(df,
                  x='Deaths_per_million',
                  y='GDP_per_capita',
                  hover_name='Country',
                  title='The Effect of GDP on Covid Deaths',
                  labels={'Deaths_per_million': 'Deaths per million',
                          'GDP_per_capita': 'GDP per capita'},
                  trendline="ols")
#fig2.update_layout(template='plotly_dark', title_x=0.5)
fig2.update_layout(title_x=0.5)
fig2.update_layout(margin=dict(t=50, r=20, l=25, b=20))

fig3 = px.scatter(df,
                  x='Persons_fully_vaccinated_per100',
                  y='GDP_per_capita',
                  hover_name='Country',
                  title='The Effect of GDP on Covid Vaccinations',
                  labels={'Persons_fully_vaccinated_per100': 'Persons Fully Vaccinated per 100',
                          'GDP_per_capita': 'GDP per capita'},
                  trendline="ols")
#fig3.update_layout(template='plotly_dark', title_x=0.5)
fig3.update_layout(title_x=0.5)
fig3.update_layout(margin=dict(t=50, r=20, l=25, b=20))

# ------------------------------------------------------------------------------
# App layout - Original

# app.layout = dbc.Container([
#
#     dbc.Row([
#         dbc.Col([
#             html.H1("A Comparison of Covid Deaths with Vaccination and Poverty Rates")
#         ], width=10)
#     ], justify="center", align='center'),
#
#     dbc.Col([
#         dbc.Card([
#             dcc.Dropdown(id='my_dropdown',
#                         options=[
#                             {'label': 'Population Fully Vaccinated (%)', 'value': 'Persons_fully_vaccinated_per100'},
#                             {'label': 'Covid deaths (per million)', 'value': 'Deaths_per_million'},
#                             {'label': 'Population Below Poverty Line (%)', 'value': 'Population_below_poverty_line'},
#                             {'label': 'GDP per Capita', 'value': 'GDP_per_capita'}
#                         ],
#                         value='Persons_fully_vaccinated_per100',
#                         multi=False,    # Disable multiple selection
#                         searchable=False,
#                         style={'text-align': 'center', 'color': 'black', 'white-space': 'nowrap'}
#                         ),
#             dcc.Graph(id='my_vaccine_map', figure=fig, className="h-100", style={'margin': 5})
#         ], style={'border-radius': '2%', 'align': 'center', 'height': '50vh'}),
#     ]),
#
#     html.Br(),
#
#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 #html.H5("The Effect of GDP on Covid Deaths", className="card-title", style={'textAlign': 'center'}),
#                 dcc.Graph(id='Scatter_plot', figure=fig2, className="h-100", style={'margin': 2})
#             ], style={'border-radius': '2%', 'align': 'center', 'height': '35vh'}),
#         ], width=6),
#
#         dbc.Col([
#             dbc.Card([
#                 #html.H5("The Effect of GDP on Covid Vaccinations", className="card-title", style={'textAlign': 'center'}),
#                 dcc.Graph(id='Scatter_plot', figure=fig3, className="h-100", style={'margin': 2})
#             ], style={'border-radius': '2%', 'align': 'center', 'height': '35vh'})
#         ], width=6),
#     ]),
#
#     html.Br()
#
# ], fluid=True)

# ------------------------------------------------------------------------------
# App layout - New

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("A Comparison of Covid Deaths with Vaccination and Poverty Rates")
        ], width=10)
    ], justify="center", align='center'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Dropdown(id='my_dropdown',
                            options=[
                             {'label': 'Population Fully Vaccinated (%)', 'value': 'Persons_fully_vaccinated_per100'},
                             {'label': 'Covid deaths (per million)', 'value': 'Deaths_per_million'},
                             {'label': 'Population Below Poverty Line (%)', 'value': 'Population_below_poverty_line'},
                             {'label': 'GDP per Capita', 'value': 'GDP_per_capita'}
                             ],
                            value='Persons_fully_vaccinated_per100',
                            multi=False,    # Disable multiple selection
                            searchable=False,
                            style={'text-align': 'center', 'color': 'black', 'white-space': 'nowrap'}
                            ),
                dcc.Graph(id='my_vaccine_map', figure=fig, className="h-100", style={'margin': 5})
            ], style={'border-radius': '2%', 'align': 'center', 'height': '90vh'}),
        ], align='center'),

        dbc.Col([
            dbc.Row([
                dbc.Card([
                    #html.H5("The Effect of GDP on Covid Deaths", className="card-title", style={'textAlign': 'center'}),
                    dcc.Graph(id='Scatter_plot', figure=fig2, className="h-100", style={'margin': 2})
                ], style={'border-radius': '2%', 'align': 'center', 'height': '44vh'}),
            ], style={'margin-right': '1%'}),

            html.Br(),

            dbc.Row([
                dbc.Card([
                    #html.H5("The Effect of GDP on Covid Vaccinations", className="card-title", style={'textAlign': 'center'}),
                    dcc.Graph(id='Scatter_plot', figure=fig3, className="h-100", style={'margin': 2})
                ], style={'border-radius': '2%', 'align': 'center', 'height': '44vh'})
            ], style={'margin-right': '1%'})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Plaintext("Data Source:\n"
                           "https://covid19.who.int/who-data/vaccination-data.csv\n"  # Population fully vaccinated per 100
                           "https://en.wikipedia.org/wiki/COVID-19_pandemic_death_rates_by_country (which uses Our World in Data)\n"  # Cumulative deaths per million
                           "https://www.cia.gov/the-world-factbook/field/population-below-poverty-line/\n"  # Population below the poverty line
                           "https://www.theglobaleconomy.com/rankings/gdp_per_capita_current_dollars/Europe/\n\n"  # GDP per capita (dollars)
                           "Last updated 21/12/2022\n"
                           "Author: Rowan Trickett",
                           style={'font-size': '70%'})
        ], width=12)
    ], justify="center", align='center'),

], fluid=True)


@app.callback(Output('my_vaccine_map', 'figure'),
              Input('my_dropdown', 'value')
)
def update_graph(value):

    fig = px.choropleth(
        data_frame=df,
        locations='ISO3',
        color=value,
        hover_name='Country',
        hover_data=['Persons_fully_vaccinated_per100', 'Deaths_per_million', 'Population_below_poverty_line',
                    'GDP_per_capita'],
        labels={'Persons_fully_vaccinated_per100': 'Fully Vaccinated (%)',
                'Deaths_per_million': 'Covid deaths (per million)',
                'Population_below_poverty_line': 'Population Below Poverty Line (%)',
                'GDP_per_capita': 'GDP per Capita'},
    )

    fig.update_layout(
        margin=dict(t=5, r=0, l=0, b=5),  # remove margins
        dragmode=False,
        geo=dict(scope='europe')  # what section of the world is being shown
    )

    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), coloraxis_colorbar_y=0, coloraxis_colorbar=dict(titleside='top'))
    fig.update_coloraxes(showscale=True, colorbar_orientation='h')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


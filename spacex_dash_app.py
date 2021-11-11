# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\Gabri\Documents\Python\Coursera IBM\SpaceX\dataset_part2.csv")
max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id = 'site-dropdown', options = [{'label': 'All Sites', 'value': 'ALL'}, {'label': 'CCSFS SLC 40', 'value': 'CCSFS SLC 40'},
                                {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'}, {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'}], value = 'ALL'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 16000, step = 1000, marks={0: '0', 2500: '2500', 5000: '5000', 10000: '10000', 15000: '15000'}, value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values = 'Class', names = 'LaunchSite', title = 'Success Site Launch Breakdown')
    else:
        data = filtered_df[filtered_df['LaunchSite'] == entered_site]
        data = pd.DataFrame(data.Class.value_counts().reset_index().values, columns = ['Class', 'Total'])
        fig = px.pie(data, values = 'Total', names = 'Class', title = f'Success rate at site {entered_site}')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property='figure'), 
[Input(component_id='site-dropdown', component_property = 'value'), Input(component_id = 'payload-slider', component_property = 'value')])

def get_scatter_chart(entered_site, payload):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['PayloadMass'] > payload[0]]
        filtered_df = spacex_df[spacex_df['PayloadMass'] < payload[1]]
        fig = px.scatter(filtered_df, x = 'PayloadMass', y = 'Class', color = 'Orbit', title = 'Success Site Launch Breakdown')
    else:
        data = filtered_df[filtered_df['LaunchSite'] == entered_site]
        data = data[data['PayloadMass'] > payload[0]]
        data = data[data['PayloadMass'] < payload[1]]
        #data = pd.DataFrame(data.Class.value_counts().reset_index().values, columns = ['Class', 'Total'])
        fig = px.scatter(data, x = 'PayloadMass', y = 'Class', color = 'Orbit', title = f'Success rate at site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

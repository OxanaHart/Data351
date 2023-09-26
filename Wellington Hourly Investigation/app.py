import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load your dataset
carbon_emissions = pd.read_csv("Carbon Emissions.csv", index_col=0)

# Calculate the 'reduction factor'
carbon_emissions['reduction factor'] = (carbon_emissions['Average Occupancy'] / 1.3 * 0.265) / (carbon_emissions['CO2emissions'])

# Create a pivot table
pivot_table = carbon_emissions.pivot_table(
    values='reduction factor',
    index='Route Variant',
    columns='Day of Week',
    aggfunc='mean'
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H2("Wellington Carbon Emissions - Oxana Hart, Jacob French"),
    dcc.Markdown("This app utilizes data provided by Metlinks NetBI app to measure carbon emissions and reductions"),
    dcc.Dropdown(
        id='route-dropdown',
        options=[{'label': route, 'value': route} for route in pivot_table.index.tolist()],
        value=pivot_table.index[0]  # Initial selection
    ),
    dcc.Graph(id='heatmap'),
])

# Define the callback to update the heatmap
@app.callback(
    Output('heatmap', 'figure'),
    Input('route-dropdown', 'value')
)
def update_heatmap(selected_route):
    filtered_pivot = pivot_table.loc[selected_route]
    fig = px.imshow(
        filtered_pivot,
        x=filtered_pivot.columns,
        y=filtered_pivot.index,
        color_continuous_scale='coolwarm',
        color_continuous_midpoint=filtered_pivot.values.max() / 2,
        zmin=0,
        zmax=filtered_pivot.values.max(),
    )
    fig.update_xaxes(title="Day of Week")
    fig.update_yaxes(title="Route Variant")
    fig.update_layout(title="Average Reduction Factor Heatmap")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




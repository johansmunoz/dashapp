import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the monthly correlation data
monthly_corr = pd.read_csv("Monthly_Correlation.csv", index_col=0, parse_dates=True)
monthly_corr.index = pd.to_datetime(monthly_corr.index.astype(str))  # Ensure index is datetime

# Filter data from March 2024 onwards
df_filtered = monthly_corr[monthly_corr.index >= "2024-03"]

# Split columns into two groups
stocks = list(df_filtered.columns)
midpoint = len(stocks) // 2
group1 = stocks[:midpoint]
group2 = stocks[midpoint:]

def create_heatmap(corr_data, group, title):
    fig = px.imshow(
        corr_data[group].T,  # Transpose for better view
        labels=dict(x="Month", y="Stock", color="Correlation"),
        title=title,
        color_continuous_scale="RdBu_r",
        aspect="auto",
    )

    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        xaxis=dict(tickangle=-45),
    )
    return fig

# Dash app setup
# Create the Dash app
app = dash.Dash(__name__)
server = app.server  # 🔥 This is required for Gunicorn to work on Render

app.layout = html.Div([
    html.H1("📊 Monthly Correlation Heatmaps", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id="group_selector",
        options=[
            {"label": "Group 1", "value": "group1"},
            {"label": "Group 2", "value": "group2"}
        ],
        value="group1",
        clearable=False,
        style={"width": "50%", "margin": "auto"}
    ),
    
    dcc.Graph(id="heatmap")
])

@app.callback(
    Output("heatmap", "figure"),
    [Input("group_selector", "value")]
)
def update_heatmap(selected_group):
    selected_stocks = group1 if selected_group == "group1" else group2
    return create_heatmap(df[selected_stocks], f"Monthly Correlation - {selected_group.capitalize()}")

# Run the server locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

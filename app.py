import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the monthly correlation data
monthly_corr = pd.read_csv("Monthly_Correlation.csv", index_col=0, parse_dates=True)
monthly_corr.index = pd.to_datetime(df.index.astype(str))  # Ensure index is datetime

# Filter data from March 2024 onwards
df_filtered = monthly_corr[monthly_corr.index >= "2024-03"]

# Split columns into two groups
stocks = list(df_filtered.columns)
midpoint = len(stocks) // 2
group1 = stocks[:midpoint]
group2 = stocks[midpoint:]

def plot_heatmap(data, title):
    fig = px.imshow(
        data.T,  # Transpose for better layout
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
    html.H1("📊 Stock Correlation Heatmaps", style={"text-align": "center"}),

    html.H3("Group 1: First Half of Stocks"),
    dcc.Graph(figure=plot_heatmap(monthly_corr, group1, "Monthly Correlation - Group 1")),

    html.H3("Group 2: Second Half of Stocks"),
    dcc.Graph(figure=plot_heatmap(monthly_corr, group2, "Monthly Correlation - Group 2")),
])

# Run the server locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

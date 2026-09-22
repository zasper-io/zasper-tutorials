import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

penguins = pd.read_csv("../data/penguins.csv").dropna()

px.scatter(
    penguins,
    x="flipper_length_mm",
    y="body_mass_g",
    color="species",
    symbol="sex",
    hover_data=["island"],
    labels={"flipper_length_mm": "Flipper length (mm)", "body_mass_g": "Body mass (g)"},
)

print(penguins)
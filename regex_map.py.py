import os
import pandas as pd
import plotly.express as px

# === Setup Output Folder ===
output_folder = "Outputs"
os.makedirs(output_folder, exist_ok=True)

# === Load Data ===
counts = pd.read_csv("Scripts/regex_counts.tsv", sep="\t")
coords = pd.read_csv("gazetteers/geonames_gaza_selection.tsv", sep="\t")

# === Clean Column Names ===
counts.columns = counts.columns.str.strip()
coords.columns = coords.columns.str.strip()

# === Rename for Consistency ===
coords = coords.rename(columns={
    "asciiname": "placename",
    "latitude": "latitude",
    "longitude": "longitude"
})

# === Merge Counts with Coordinates ===
data = pd.merge(counts, coords, on="placename")

# === Ensure Proper Data Types ===
data["count"] = pd.to_numeric(data["count"], errors="coerce")
data = data.dropna(subset=["count", "latitude", "longitude"])

# === Create Animated Map ===
fig = px.scatter_mapbox(
    data,
    lat="latitude",
    lon="longitude",
    hover_name="placename",
    size="count",
    animation_frame="month",
    color="count",
    color_continuous_scale=px.colors.sequential.YlOrRd,
    title="Regex-Extracted Place Mentions Over Time",
    zoom=8,
    height=600,
    mapbox_style="carto-positron"  # English labels
)

fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

# === Save HTML Map ===
html_path = os.path.join(output_folder, "regex_map.html")
try:
    fig.write_html(html_path)
    print(f"HTML map successfully saved to: {html_path}")
except Exception as e:
    print(f"Error saving HTML map: {e}")

# === Save PNG Image (Requires kaleido) ===
png_path = os.path.join(output_folder, "regex_map.png")
try:
    fig.write_image(png_path, engine="kaleido")
    print(f"PNG image successfully saved to: {png_path}")
except Exception as e:
    print(f"Error saving PNG image: {e}")

# === Display the Map ===
fig.show()

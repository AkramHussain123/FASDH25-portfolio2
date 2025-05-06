import os
import pandas as pd
import plotly.express as px

# Create a folder named "Outputs" to save the map files
output_folder = "Outputs"
os.makedirs(output_folder, exist_ok=True)

# Read the place mention counts from the TSV file
counts = pd.read_csv("regex_counts.tsv", sep="\t")

# Read the place coordinates from the gazetteer TSV file
coords = pd.read_csv("../gazetteers/geonames_gaza_selection.tsv", sep="\t")


# Remove any extra spaces from column names
counts.columns = counts.columns.str.strip()
coords.columns = coords.columns.str.strip()

# Rename the 'asciiname' column so it matches the name in counts
coords = coords.rename(columns={
    "asciiname": "placename",
    "latitude": "latitude",
    "longitude": "longitude"
})

# Combine the counts with their matching coordinates
data = pd.merge(counts, coords, on="placename")

# Make sure count values are numbers and remove rows with missing values
data["count"] = pd.to_numeric(data["count"], errors="coerce")
data = data.dropna(subset=["count", "latitude", "longitude"])

# Create an animated map showing place mentions over time
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
 
)
mapbox_style="carto-positron"  # Selected with help from ChatGPT (OpenAI) for clean English map labels, previously the code had some issue and the language was Persian instead of english.

# Remove extra space around the map for more precision and clarity
fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

# Save the map as an interactive HTML file so that I can access it and perfom zoom in, out etc
html_path = os.path.join(output_folder, "regex_map.html")
try:
    fig.write_html(html_path)
    print(f"HTML map successfully saved to: {html_path}")
except Exception as e:
    print(f"Error saving HTML map: {e}")

# Save the map as a PNG image (needs kaleido installed)
png_path = os.path.join(output_folder, "regex_map.png")
try:
    fig.write_image(png_path, engine="kaleido")
    print(f"PNG image successfully saved to: {png_path}")
except Exception as e:
    print(f"Error saving PNG image: {e}")

# Show the map in the browser for making it more interactive and clear. 
fig.show()

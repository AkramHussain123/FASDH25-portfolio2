import pandas as pd
import plotly.express as px

# Load data
ner_counts = pd.read_csv("C:/Users/admin/Downloads/FASDH25-portfolio2/Scripts/ner_counts.tsv", sep="\t")
coordinates = pd.read_csv("C:/Users/admin/Downloads/FASDH25-portfolio2/gazetteers/NER_gazetteer.tsv", sep="\t")


# Clean column names
ner_counts.columns = ner_counts.columns.str.strip()
coordinates.columns = coordinates.columns.str.strip()

# renaming columns in coordinates to match ner_counts and plotting requirements
ner_counts = ner_counts.rename(columns={"name": "placename", "frequency": "ner_count"})
coordinates = coordinates.rename(columns={"Name": "Place", "Latitude": "latitude", "Longitude": "longitude"})

# Function to clean coordinate values
# Assistance from other group
def clean_coordinate(coord):
    if isinstance(coord, str):
        # Remove degree symbols, quotes, etc.
        coord = coord.split('°')[0]
        coord = coord.split('′')[0]
        coord = coord.split('"')[0]
        # Handle cases like "35.1231°" which becomes "35.1231"
        try:
            return float(coord)
        except ValueError:
            return None
    return coord


coordinates['latitude'] = coordinates['latitude'].apply(clean_coordinate)
coordinates['longitude'] = coordinates['longitude'].apply(clean_coordinate)


# Rename columns in coordinates to match ner_counts and plotting requirements
ner_counts = ner_counts.rename(columns={"name": "placename", "frequency": "ner_count"})
coordinates = coordinates.rename(columns={"Name": "Place", "Latitude": "latitude", "Longitude": "longitude"})
# Merge data on 'placename'
data = pd.merge(ner_counts, coordinates, left_on="placename", right_on="Place")


# Assitance from Mathew
# Ensure 'ner_count' is numeric and drop rows with missing values
data["count"] = pd.to_numeric(data["ner_count"], errors="coerce")
data = data.dropna(subset=["ner_count", "latitude", "longitude"])

fig = px.scatter_map(
    data,
    lat="latitude",
    lon="longitude",
    hover_name="Place",
    size="count",
    color="count",
    title="NER-extracted Places",
    zoom=2,
)

fig.show()

# Save map to an HTML file
fig.write_html("NER_map.html")
fig.write_image("ner_map.png")


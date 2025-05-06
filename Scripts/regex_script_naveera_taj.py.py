'''This is your starting script for today's Python class.

This script contains the code we wrote last week
to count the number of times each place in Gaza
is mentioned in our corpus.

Now, we want to store this count into a tsv file.

I have written a function (write csv) to do this -
but it has some mistakes in it.

Please fix the mistakes and call the function
to write the 

'''
# Import required libraries
import re            # For regular expressions
import os            # For working with folders and files
import pandas as pd  # For creating and saving tables as TSV

# ===== Function to Write Output to TSV File =====
def write_tsv(rows, column_list, path):
    # Convert the data rows into a DataFrame (table)
    df = pd.DataFrame(rows, columns=column_list)
    # Save the table to a .tsv file
    df.to_csv(path, sep="\t", index=False)

# ===== File Paths =====
# Folder that contains article text files
folder = "../articles"

# Gazetteer file with place names and alternate names
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"

# File path for the output .tsv
output_path = "regex_counts.tsv"

# ===== Load Gazetteer and Create Regex Patterns =====
patterns = {}  # Dictionary to store place name and regex pattern

# Open and read the gazetteer file
with open(gazetteer_path, encoding="utf-8") as f:
    lines = f.read().split("\n")  # Split the file into lines

# Skip the header and loop through each line
for row in lines[1:]:
    columns = row.split("\t")  # Split the row into columns

    if len(columns) < 6:
        continue  # Skip rows that don't have enough columns

    asciiname = columns[0].strip()  # Main name of the place
    alternate_names = columns[5].strip()  # Alternate names (comma-separated)

    name_variants = [asciiname]  # Start with main name

    # If alternate names exist, split and add them to list
    if alternate_names:
        for alt in alternate_names.split(","):
            alt = alt.strip()
            if alt:
                name_variants.append(alt)

    # Escape any special characters in names for regex
    escaped_variants = [re.escape(name) for name in name_variants]

    # Create a regex pattern that matches any of the name variants
    # \b ensures whole-word matches only
    pattern = r"\b(" + "|".join(escaped_variants) + r")\b"

    # Store the regex pattern and initialize count to 0
    patterns[asciiname] = {"pattern": pattern, "count": 0}

# ===== Prepare to Count Mentions by Month =====
mentions_per_month = {}  # Dictionary to store results

# Articles before this date will be skipped
war_start_date = "2023-10-07"

# ===== Process Each Article in the Folder =====
for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue  # Skip files that are not .txt

    date_str = filename.split("_")[0]  # Extract date from filename

    if date_str < war_start_date:
        continue  # Skip files from before the war started

    # Read the content of the article
    with open(os.path.join(folder, filename), encoding="utf-8") as f:
        text = f.read()

    # Search for each place name pattern in the text
    for place in patterns:
        regex = patterns[place]["pattern"]  # Get the regex pattern
        matches = re.findall(regex, text, re.IGNORECASE)  # Find all matches (case-insensitive)
        count = len(matches)  # Count number of mentions

        patterns[place]["count"] += count  # Update total count

        if count > 0:
            # Get the year and month (YYYY-MM) from the date
            month_str = date_str[:7]

            # Create new dictionary entries if not already there
            if place not in mentions_per_month:
                mentions_per_month[place] = {}
            if month_str not in mentions_per_month[place]:
                mentions_per_month[place][month_str] = 0

            # Add this article’s mentions to the total for that month
            mentions_per_month[place][month_str] += count

# ===== Print the Results in Dictionary Format =====
for place in mentions_per_month:
    print(f'"{place}": {{')
    months = list(mentions_per_month[place].keys())

    for month in months:
        count = mentions_per_month[place][month]
        # Print month and count, use comma except for last item
        comma = "," if month != months[-1] else ""
        print(f'    "{month}": {count}{comma}')
    print("},")

# ===== Convert Data to Rows for TSV Output =====
rows = []  # List of rows (place, month, count)

for place in mentions_per_month:
    for month in mentions_per_month[place]:
        count = mentions_per_month[place][month]
        rows.append((place, month, count))  # Add row to list

# ===== Write Results to Output File =====
write_tsv(rows, ["placename", "month", "count"], output_path)




                                



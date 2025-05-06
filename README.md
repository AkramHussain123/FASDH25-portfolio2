# FASDH25-portfolio2
A repository for students' portfolios for mini-project 2

# Mapping Gaza During the War: Visualizing Place Mentions Over Time Using Regex and NER
This project analyzes and maps place names mentioned in news articles about the ongoing war in Gaza.It uses two methods to extract toponyms from text: regular expressions with a gazetteer, and Named Entity Recognition (NER) with NLP tools. Extracted place names are geocoded to retrieve their latitude and longitude coordinates. The frequency of place mentions is tracked by month to observe shifts in geographic focus over time. The results are visualized using interactive and static maps generated with Plotly Express. The project highlights the strengths and limitations of both extraction methods. All code, data, and visualizations are organized for reuse and further analysis.

## Project Structure/file path

FASDH25-portfolio2/
├── articles/ # News article corpus (YYYY-MM-DD format)
├── gazetteers/
│ ├── geonames_gaza_selection.tsv # Original gazetteer
│ └── NER_gazetteer.tsv # Generated NER gazetteer
├── scripts/
│ ├── build_gazetteer.py # Gazetteer construction script 
│ ├── copy_of_Gaza_NER2_kamil_faizan.ipynb # NER extraction notebook 
│ ├── regex_script_final.py # Final regex extraction script
│ └── regex_mapping.py # Regex-based mapping script
│ │
│ ├── regex_counts.tsv # Regex-extracted frequencies
│ ├── ner_counts.tsv # NER-extracted frequencies
│ ├── regex_map.html # Regex interactive visualization
│ ├── regex_map.png # Regex static visualization
│ ├── ner_map.html # NER interactive visualization
│ └── ner_map.png # NER static visualization
└── README.md # This documentation conatins the README file we have collectively created for our project.

## Regex and Gazetteer-Based Place Name Extraction
This part of the project was focused on identifying place names in Gaza mentioned in news articles using regular expressions and a gazetteer. To improve recall, the script goes beyond exact matches by incorporating alternative spellings and name variants found in the gazetteer. It processes only articles related to the current war (filtered by date), counts how often each place is mentioned per month, and saves the data to a file (regex_counts.tsv). The result is a structured dataset that reflects the changing geographic focus of news coverage over time.
 
## Regex-Based Place Name Extraction with Gazetteer Integration 
This part of the project was focused on the extraction of Gaza-related place names from a large corpus of news articles using regular expressions and a gazetteer. By adapting the script from class notes, I modified it to work with the larger corpus and gazetteer in the portfolio repository. I improved recall by using not only the asciiname column but also alternative names from the gazetteer to build more inclusive regex patterns. I also added functionality to filter out articles written before the current conflict based on their filenames. The script then counts how often each place is mentioned per month and organizes the results into a nested dictionary. Finally, it outputs the data into a tab-separated values file (regex_counts.tsv), providing a clear monthly breakdown of place name mentions throughout the conflict.

###  Mapping Regex-Extracted Place Mentions in Gaza Over Time
This part of the project was focused on mapping the place names extracted through regex onto an animated, interactive map using Plotly Express. By adapting and extending the visualization techniques introduced in class, I used the data stored in regex_counts.tsv to create a time-based map that shows how frequently each Gaza location was mentioned across different months. I experimented with various display options—such as color gradients, point sizes, and map styles—and decided that using circle size and color intensity to represent mention frequency offered the clearest and most informative visual. The map was exported both as an interactive HTML file (regex_map.html) and a static PNG image (regex_map.png) for flexibility in presentation.
 
## Named Entity Recognition (NER) for Extracting and Counting Place Mentions  Articles
This part of the project focused on identifying and counting place names mentioned in news articles from January 2024 using Named Entity Recognition (NER) techniques. The goal was to extract location entities, normalize variations in naming (such as apostrophes or alternate forms), and avoid redundant counting of the same place under slightly different names. To begin, we copied the Gaza-NER2 script from the shared class drive via Google Colab, renamed it to include all group members’ names, and removed unnecessary portions of the code to streamline our workflow.

We then set up the environment by installing necessary libraries such as stanza, os, requests, and time, and initialized a pipeline for entity recognition. After cloning the required repository, we focused on processing the articles dated January 2024, using the NER model to extract place names. A key part of our implementation involved designing logic to handle and merge different textual variants of the same place, ensuring accurate and non-redundant counts.

Finally, we saved the structured results—containing place names and their mention frequencies—into a .tsv file, which we then committed and pushed to our GitHub repository using Git Bash, as practiced in class.
### Mapping The NER outputs
This part of the project aimed to visualize the frequency of place names extracted through Named Entity Recognition (NER) from January 2024 news articles. Using the data stored in the ner_counts.tsv file, we utilized Plotly Express to create an interactive map that plots the frequencies of place mentions. To accurately map these places, we combined the extracted place names with their corresponding coordinates, which were sourced from the NER_gazetteer.tsv file.

The map was designed to be interactive and animated, displaying how the mentions of various places evolved over time in the articles. We saved the final map as both an interactive HTML file (ner_map.html) and a static PNG image (ner_map.png) to facilitate easy sharing and presentation. The approach provided a clear, visual representation of place name distributions and trends over the given time period.

## Geocoding NER-Extracted Place Names with Manual Additions
The first file I used to generate a gazetteer from the NER result was ner_counts.tsv, which included location names that were taken from news articles using a Named Entity Recognition (NER) tool. To automatically geocode these location names and extract their latitude and longitude, I then created a script that used the geopy library. I looked up the coordinates of some locations(Morocco, Israel, Indonesia, Kollupitiya, Colombo, Ash-Shawawra, Palestine, Mezzeh, Damascus, Syria, Yemen, Nabatieh, Lebanon, Yir'on, Israel, Goren, Israel, Dahiyeh (Southern Beirut Suburbs), Washington, D.C., USA, Sistan and Baluchestan, Iran, Beirut, Lebanon, Shatila, Beirut, France), by hand using Google and added them to the finished TSV file when the script was unable to resolve them. A gazetteer guarantees uniform spelling and locations but could overlook context-specific or unique items, whereas NER is useful for catching unexpected or new locales.
Some of the names such as "@MirandaCleland", "@majedalansari", "Thameen Darby", "Mercator", "Darby’s Nakba", "Houthis", "Hamas", "Khreis", and "Salameh", refer to individuals or organizations rather than specific geographic locations, so precise coordinates are not applicable so left them as it is.

## Advantages and Disadvantages of the Methods used
### Regex + Gazetteer Approach
#### Advantages:
The regex and gazetteer approach offers significant customizability, allowing for fine-tuned control over how place names are identified. By incorporating alternative spellings and variations from the gazetteer, the script can capture a wider range of place names, improving recall. The approach doesn’t rely on external models or libraries, meaning it operates independently and is simpler to implement. Additionally, regex is fast and efficient, processing large corpora quickly without the overhead of machine learning models. Another benefit is the full transparency and control over the extraction process, which allows for manual adjustments and troubleshooting when necessary, providing more precise results tailored to the specific dataset.

#### Disadvantages:
However, the regex and gazetteer approach has limitations in that it is confined to predefined patterns and place names. New or unexpected variations in place names may go unrecognized unless manually added, making the approach less adaptable to evolving datasets. Moreover, regex patterns that are too broad can lead to false positives, where unrelated terms are mistakenly identified as place names. Additionally, the method lacks context-awareness, meaning it can’t differentiate between instances where a place name might have different meanings or uses in different contexts. Finally, manual updates to the gazetteer and regex patterns are required to maintain accuracy, making the process time-consuming and less scalable.

### NER Approach
#### Advantages:
NER offers significant advantages in its ability to recognize place names in context, which improves the overall accuracy by distinguishing between different places that may share similar names. The method is fully automated, meaning there is no need for manual definition of patterns, and it can easily scale to handle large datasets. The NER approach can also capture new and previously unseen place names, providing a robust solution for dynamic datasets. Additionally, the model’s contextual understanding allows it to adapt to variations in how place names are written or mentioned across articles, making it flexible and effective for a variety of texts. Once set up, NER can process a large volume of articles efficiently.

#### Disadvantages
On the downside, NER models can struggle with accuracy if not properly trained on a relevant corpus, potentially missing or misidentifying place names. The process is computationally more intensive than regex, requiring more resources and time, particularly when working with large datasets. Furthermore, setting up an NER pipeline can be complex, requiring specific libraries, models, and configurations that may be challenging for users without prior machine learning experience. NER models can also be prone to overfitting or underfitting, leading to either missed place names or incorrect identifications, especially when dealing with complex, unstructured text such as news articles.

## Maps image PNG
#### Regex generated Image PNG:
![alt text(https://github.com/AkramHussain123/FASDH25-portfolio2/blob/main/Scripts/regex_map.png)] 

#### NER generated Image PNG: 

## comparsion of the two maps on the basis of our experince with developing this project
The Regex Map uses regular expressions to capture place names in a very flexible way, including different spellings, variations, and even lesser-known locations. Because it's based on a gazetteer, it can pick up many variations of a place name, like “Khan Younis” vs. “KhanYounis” or “Khan Yunis.” This approach gives a broad view of the geographic mentions, but it can also make the map look a bit crowded, since it includes so many variants. Plus, it depends heavily on the gazetteer, meaning that any new place names or variations require manual updates, which can be a bit time-consuming.

On the other hand, the NER Map uses Named Entity Recognition to automatically pull out place names from the articles, giving a cleaner and more organized map. It's more focused on well-known, standard place names, which makes it look less cluttered and more precise. However, the downside is that it may miss variations or new place names, especially those not included in its training data. While it’s easier to use and doesn't require as much manual work, it can’t always pick up every place, especially those that aren’t common or have unusual spellings.

The Regex Map captures a wider range of places, but it can look a little messy and needs more manual effort to keep up-to-date. The NER Map, on the other hand, gives a smoother, more polished map but might miss out on some places that don't match its predefined patterns. It’s a trade-off between getting a full picture with regex or a more refined but possibly incomplete view with NER.


















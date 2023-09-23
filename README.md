# Project: E7 Hero Data

## Introduction

"E7 Hero Data" is a personal project which involves web scraping, data analysis, visualization, and the creation of an interactive web dashboard. This project is dedicated to extracting, analyzing, and presenting data related to characters from the game Epic Seven. 

For some context, Epic Seven is a turn-based strategy game developed by a Korean game company Smilegate. In a fight, heroes take turns to use their ability to deal damage, heal or provide utility such as buffing allies and debuffing enemies. Each heroes would have a rarity from 1 to 5 Stars; though 1 and 2 stars heroes are rarely use in a fight but rather as fodders to upgrade other heroes so I have omitted them from this project. Together with Class and Horoscope, the base stats of a hero could be determined; with some exceptions such as Summertime Iseria having a 30% atk increase from her Passive skills. This project aims to display the relationships between each of the factors and explores how each stats relate to one anothers.

## Part 1: Data Extraction (e7xscrape.py)

The project begins with the script `e7xscrape.py`, which serves as the foundation for gathering character data. Here's a summary of its role in the project and its associated code:

Firstly, I import the necessary modules
```
import collections.abc
collections.Callable = collections.abc.Callable

import urllib.parse, urllib.error, urllib.request
from bs4 import BeautifulSoup
import ssl
import json
import re
import pandas as pd
```

- **Web Scraping**: The script uses web scraping techniques to access character information from the website "https://epic7x.com/characters/."

- **Data Parsing**: With the help of the `BeautifulSoup` library, it parses the HTML content of the website to locate a specific script tag containing character data in JSON format.

- **Data Extraction**: Character attributes such as name, link, rarity, class, horoscope, attack, health, defense, and speed are extracted from the JSON data.

- **Additional Statistics**: Individual HTTP requests to character-specific URLs are made to retrieve further character statistics.

- **Data Organization**: Extracted data is organized into a structured format.

- **Data Storage**: The script saves the organized data in a Pandas DataFrame and exports it as a CSV file named "e7HeroData.csv."

## Part 2: Data Visualization (e7visualization.py)

The next step in the project involves the script `e7visualization.py`, which focuses on the visual representation of character data. Here's an overview of its role:

- **Data Import**: The script imports the character data from the previously generated "e7HeroData.csv" file using the Pandas library.

- **Data Categorization**: It defines filters and criteria for categorizing characters based on attributes like rarity, class, and horoscope.

- **Statistics Calculation**: For each filter, the script calculates percentile values for specific character statistics, such as attack, health, defense, etc.

- **Visualization**: The key aspect of this script is the creation of line plots that visualize how character statistics vary across different categories.

- **Plot Storage**: The resulting plots are saved as PDF files, each illustrating the variation of a specific statistic (e.g., attack) across different character categories (e.g., rarity).

- **Exploratory Analysis**: The script is designed for exploratory data analysis and helps users understand the distribution of character statistics within the game.

## Part 3: Interactive Web Dashboard (e7dash.py)

The final component of the "E7 Hero Data" project is the interactive web dashboard created using the script `e7dash.py`. This part ties everything together:

- **Dash Framework**: The script utilizes the Dash framework to create an interactive web interface.

- **User Interface**: It sets up a user-friendly interface with elements like dropdown menus, buttons, and images.

- **Callback Functions**: Dash callbacks are defined to handle user interactions. For example, selecting different filters or statistics updates the displayed character image, comment, and download link.

- **Smooth Scrolling**: An additional callback allows for smooth scrolling to an "About" section when the "About" button is clicked.

- **Deployment**: The Dash app is deployed, making character data accessible and interactive via a web interface.

## Conclusion

The "E7 Hero Data" project seamlessly combines web scraping, data analysis, visualization, and web development to create a comprehensive platform for exploring and understanding character data from the "E7" game or application. Users can interact with the data through the web dashboard, explore character statistics, and gain valuable insights into the game's characters. This project showcases how data extraction, analysis, and visualization can be transformed into an engaging and informative user experience.

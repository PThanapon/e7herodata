# Project: E7 Hero Data

## Introduction

"E7 Hero Data" is a personal project which involves web scraping, data analysis, visualization, and the creation of an interactive web dashboard. This project is dedicated to extracting, analyzing, and presenting data related to characters from the game Epic Seven. 

For some context, Epic Seven is a turn-based strategy game developed by a Korean game company Smilegate. In a fight, heroes take turns to use their ability to deal damage, heal or provide utility such as buffing allies and debuffing enemies. Each heroes would have a rarity from 1 to 5 Stars; though 1 and 2 stars heroes are rarely use in a fight but rather as fodders to upgrade other heroes so I have omitted them from this project. Together with Class and Horoscope, the base stats of a hero could be determined; with some exceptions such as Summertime Iseria having a 30% atk increase from her Passive skills. This project aims to display the relationships between each of the factors and explores how each stats relate to one anothers.

## The Process 

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

- **Web Scraping**: The script uses `urllib` library to access character information from the website "https://epic7x.com/characters/."

```
url = "https://epic7x.com/characters/"
request_site = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(request_site, context=ctx).read()
```

- **Data Parsing**: With the help of the `BeautifulSoup` library, I parses the HTML content of the website to locate a specific script tag containing the hero data in JSON format, in this case, it is in the 9th script tags. As the data is stored in the form of Javascripts array with an object for each characters, I sliced the string (obtained from `BeautifulSoup`) into just the array and use Regex (`re`) to match each Javascript object, hence the non-greediness.
```
tags = soup("script")
counter = 0
for tag in tags:
    if counter == 8:
        new_tag = f'{tag}'
        break
    counter += 1

cleaned = new_tag[152:106439].rstrip()
result = re.findall("\{.*?\}", cleaned)
```

![](https://media.discordapp.net/attachments/844184695754457122/1155085988952023050/image.png?width=1666&height=993 "Here's how the arrary look like")

<div align="center"> Here's how the array look like </div>

&nbsp;

- **Data Extraction**: Character attributes such as name, link, rarity, class, horoscope, attack, health, defense, and speed are extracted from the string. The names are stored as the keys in the dictionary which itself containes a dictionary with 2 keys; "link" and "info". The link stored will allow us to go to a specific page on the epic7x site which contain more information about a character, while info store information about the characters such rarity, class, etc. Note: the exception for "Support Model Brinus" is due to her being an unreleased character but as the model is teased in game, some information about the character is listed on the site but there is not stat associated.

```
dict = {}
for res in result:   
    icon = res.index("icon")
    
    if res[9:icon-3] == "Support Model Brinus":
        continue 

    link = res.index('link')
    rar = res.index("rarity")
    cla = res.index("class")
    ele = res.index("element")
    hor = res.index("horoscope")
    max = res.index("max")
    att = res.index("attack")
    hea = res.index("health")
    defe =res.index("defense")
    spd = res.index("speed")
    link_end = res.index('","stats')
    dict[f"{res[9:icon-3]}"] = {}
    dict[f"{res[9:icon-3]}"]["link"] = res[link+7:link_end].replace("\/", "/")
    dict[f"{res[9:icon-3]}"]["info"] = {}
    dict[f"{res[9:icon-3]}"]["info"]["rarity"] = res[rar+9]
    dict[f"{res[9:icon-3]}"]["info"]["class"] = res[cla+8:ele-3]
    dict[f"{res[9:icon-3]}"]["info"]["horoscope"] = res[hor+12:link-3]  
    dict[f"{res[9:icon-3]}"]["info"]["attack"] = int(res[att+9:hea-3])
    dict[f"{res[9:icon-3]}"]["info"]["health"] = int(res[hea+9:defe-3])
    dict[f"{res[9:icon-3]}"]["info"]["defense"] = int(res[defe+10:spd-3])
```

- **Additional Statistics**: Individual HTTP requests to character-specific URLs are made to retrieve further character statistics, using the links from the previous dictionary. Now the data we want are in the table row tag. Notice how the position of tr tag we chose depends on the rarity of the units. This is due to the way the leveling system in Epic Seven works so more stat are stored in the website epic7x for lower rarity character and hence we need to go through more table. Additionally, some heroes gain some stat through the process of "awakening" which the site store the increase in bracket so we have to also account for that.
  

```
for char in dict:
    char_link = dict[char]["link"]
    request_site = urllib.request.Request(char_link, headers={"User-Agent": "Mozilla/5.0"})

    html = urllib.request.urlopen(request_site, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup("tr")
    i = 0

    if dict[char]["info"]["rarity"] == "5":
        for tag in tags:
            if i == 7:
                stat_table = tag
            i += 1
    elif dict[char]["info"]["rarity"] == "4":
        for tag in tags:
            if i == 9:
                stat_table = tag
            i += 1
    elif dict[char]["info"]["rarity"] == "3":
        for tag in tags:
            if i == 11:
                stat_table = tag
            i += 1

    stat = []
    try:
        for child in stat_table.children:
            try:
                for kid in child.children:
                    try:
                        for baby in kid.children:
                            if f"{baby}"[0] != " ":
                                try:
                                    new_baby = int(baby)
                                except:
                                    new_baby = int(baby[:-1])
                                stat.append(new_baby)
                            else:
                                start = baby.index("(") +1
                                try:
                                    end = baby.index("%")
                                except:
                                    end = baby.index(")")
                                stat[prev] += int(baby[start:end])
                            prev = len(stat) - 1 
                    except:
                        pass
            except:
                pass
    except:
        pass
```

- **Data Organization**: Extracted data is organized into a structured format and stored in the previous dictoionary using the key corresponding to the character name. The length of the dictionary is checked so that there are no missing values.

```
    dict[char]["info"]["crit chance"] = stat[0]
    dict[char]["info"]["crit damage"] = stat[1]
    dict[char]["info"]["effectiveness"] = stat[2]
    dict[char]["info"]["effectiveness resistance"] = stat[3]
    dict[char]["info"]["speed"] = stat[4]

    if len(dict[char]["info"]) != 11:
        print(f"Len Mismatch for {char}, {dict[char]['info']}")
        break
```

- **Data Storage**: The script saves the organized data in a Pandas DataFrame and exports it as a CSV file named "e7HeroData.csv." 

```
df = pd.DataFrame(new_dict)
df.to_csv(f"e7HeroData.csv")
```

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

Initially, I wasn't planning to make a dashboard for this project. However, after taking an AI literacy course, I started to wonder if I could use AI to make this project better. So thats exactly what I asked ChatGPT

```
Me:
how should i improve the code above and analyze the data better

ChatGPT:
[omitted]
10. Interactive Dashboard:
Create an interactive dashboard using tools like Dash (for web-based apps)
or Jupyter Widgets to allow users to explore the data interactively.
[omitted]
```
However, I have never made a web-based dashboard using python before so I tried to prompt it further for more specific instruction. After hours of fine-tuning, this is the result:

- **Dash Framework**: The script utilizes the Dash framework to create an interactive web interface.

- **User Interface**: It sets up a user-friendly interface with elements like dropdown menus, buttons, and images.

- **Callback Functions**: Dash callbacks are defined to handle user interactions. For example, selecting different filters or statistics updates the displayed character image, comment, and download link.

- **Smooth Scrolling**: An additional callback allows for smooth scrolling to an "About" section when the "About" button is clicked.

- **Deployment**: The Dash app is deployed, making character data accessible and interactive via a web interface.

## Conclusion

The "E7 Hero Data" project seamlessly combines web scraping, data analysis, visualization, and web development to create a comprehensive platform for exploring and understanding character data from the "E7" game or application. Users can interact with the data through the web dashboard, explore character statistics, and gain valuable insights into the game's characters. This project showcases how data extraction, analysis, and visualization can be transformed into an engaging and informative user experience.

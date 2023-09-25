# Project: E7 Hero Data

## Introduction

"E7 Hero Data" is a personal project which involves web scraping, data analysis, visualization, and the creation of an interactive web dashboard. This project is dedicated to extracting, analyzing, and presenting data related to characters from  Epic Seven. 

For some context, Epic Seven is a turn-based strategy game developed by a Korean game company Smilegate. In a fight, heroes take turns to use their ability to deal damage, heal or provide utility such as buffing allies and debuffing enemies. Each heroes would have a rarity from 1 to 5 Stars; though 1 and 2 stars heroes are rarely use in a fight but rather as fodders to upgrade other heroes so I have omitted them from this project. Together with Class and Horoscope, the base stats of a hero could be determined; with some exceptions such as Summertime Iseria having a 50% atk increase from her Passive skills. This project aims to display the relationships between each of the factors and explores how each stats relate to one anothers. (Side note: from the picture, you might notice that theres are "equipments" that each hero can equip. These could give either a flat or a percentage increase based on the base stat. Hence, this is why it is why it is important for a hero to have a high base stat)

![](https://cdn.discordapp.com/attachments/844184695754457122/1155190810887856138/Screenshot_20230924-011148_Epic_Seven.jpg "Summertime Iseria")

<div align="center"> Summertime Iseria, a 5 Star, Capricorn, Ranger </div>

&nbsp;

## Key Findings

**WORK IN PROGRESS**

## The Process 

## Part 1: Data Extraction ( [e7xscrape.py](https://github.com/pthanapon/e7herodata/blob/main/e7xscrape.py) )

The project begins with `e7xscrape.py`, which serves as the foundation for gathering character data. Here's a summary of its role in the project:

Firstly, I import the necessary modules
```
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
```

- **Web Scraping**: The script uses `urllib` library to access character information from the website "https://epic7x.com/characters/."

```
url = "https://epic7x.com/characters/"
request_site = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(request_site).read()
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

## Part 2: Data Visualization ( [e7visualization.py](https://github.com/pthanapon/e7herodata/blob/main/e7visualization.py) )

In this section, we delve into the script `e7visualization.py`, which is dedicated to the visual representation of character data. Here's an outline of its role:

- **Data Import**: The script leverages the Pandas library to import character data from the "e7HeroData.csv" file.

- **Data Categorization**: It establishes filters and criteria to categorize characters based on attributes like rarity, class, and horoscope.

- **Statistics Calculation**: For each filter, the script calculates percentile values for specific character statistics such as attack, health, defense, etc.

- **Visualization**: A key feature of this script is the creation of line plots that visually demonstrate how character statistics vary across different categories.

&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![](https://cdn.discordapp.com/attachments/844184695754457122/1155136996247863296/image.png "Speed by class")

<div align="center"> Distribution of Speed by Class </div>

&nbsp;

- **Plot Storage**: The resulting plots are stored as PDF files, each depicting the variation of a specific statistic (e.g., attack) across distinct character categories (e.g., rarity).

- **Exploratory Analysis**: This script is designed for exploratory data analysis, enabling users to comprehend the distribution of character statistics within the game. It utilizes the Matplotlib library for visualization.

## Part 3: Additional Data Analysis ( [e7supplementary.py](https://github.com/pthanapon/e7herodata/blob/main/e7supplementary.py) )

This section introduces the script `e7supplementary.py`, which enhances the project with additional data analysis. Here's an overview of its role, distinguishing it from Part 2:

- **Data Import**: The script imports character data from the "e7HeroData.csv" file using the Pandas library.

- **Mean Calculation**: It computes the mean values for specific character statistics, including attack, health, defense, crit chance, crit damage, effectiveness, effectiveness resistance, and speed.

- **Data Grouping**: The script groups the data based on filter criteria such as rarity, class, and horoscope.

- **Visualization**: For each statistic, it generates a series of bar plots, one for each filter, to visualize the average value of that statistic across various categories.

&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ![](https://media.discordapp.net/attachments/844184695754457122/1155135429071343737/image.png?width=661&height=993 "Attack Averages")

<div align="center"> Mean of Attack based on Rarity, Class and Horoscope </div>

&nbsp;

- **Plot Storage**: The resulting plots are saved as image files, each illustrating the average value of a specific statistic by category.

Unlike Part 2, which utilizes Matplotlib for visualization, Part 3 employs the Seaborn library to create these informative visualizations.

Together, these sections offer a comprehensive approach to character data analysis, allowing users to explore character statistics from different perspectives and gain valuable insights into the game's characters.

## Part 4: Interactive Web Dashboard ( [e7dash.py](https://github.com/pthanapon/e7herodata/blob/main/e7dash.py) )

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

![](https://cdn.discordapp.com/attachments/844184695754457122/1155135109524103268/image.png "E7 Hero Data Dashboard")

<div align="center"> E7 Hero Data Dashboard </div>

&nbsp;

- **Dash Framework**: The script utilizes the Dash framework to create an interactive web interface.

- **User Interface**: It sets up a user-friendly interface with elements like dropdown menus, buttons, and images.

- **Callback Functions**: Dash callbacks are defined to handle user interactions. For example, selecting different filters or statistics updates the displayed character image, comment, and download link.

![](https://media.discordapp.net/attachments/844184695754457122/1155921908450213898/image.png?width=1075&height=572 "E7 Hero Data Dashboard")

<div align="center"> Dropdown Menu for stat options </div>

&nbsp;  


- **Smooth Scrolling**: An additional callback allows for smooth scrolling to an "About" section when the "About" button is clicked.

- **Deployment**: The Dash app is deployed locally through localhost, making character data accessible and interactive via a web interface. (I have tried deploying with Heroku but it will cost $7 per month so I took it down)


## Part 5: Challenges Faced

Throughout the development of the "E7 Hero Data" project, I encountered several challenges that required problem-solving and troubleshooting. Here, I outline two notable challenges and how I addressed them:

### Challenge 1: Handling Different Data Structures for 4-Star and 3-Star Heroes

One of the unexpected challenges arose from the fact that character data for 4-star and 3-star heroes on the Epic Seven website was stored differently compared to 5-star heroes. This difference in data structure led to missing stat values in the initial data extraction process. To overcome this challenge:

- **Troubleshooting**: I began by carefully inspecting the content of the `<tr>` (table row) tags on the web pages where hero statistics were stored. This involved printing multiple equal signs (`======`) in a line to distinguish between each tag and understand the structure of the data.

- **Selective Data Retrieval**: After identifying the variations in data storage, I adapted the code to selectively retrieve data based on the rarity of the heroes. For example, I used different indices for 4-star and 3-star heroes, ensuring that the correct data was extracted for each rarity level.

- **Data Validation**: To ensure data integrity, I implemented validation checks to confirm that the extracted data matched the expected structure. This involved verifying that all required statistics were present and correctly stored in the dictionary.

### Challenge 2: Dealing with FutureWarning in Seaborn Library

When I incorporated the Seaborn library for data visualization, I encountered a recurring FutureWarning message. This warning was related to certain aspects of data visualization in Seaborn. To resolve this issue:

![](https://media.discordapp.net/attachments/844184695754457122/1155193468340142150/image.png?width=1920&height=740 "FutureWarning")

<div align="center"> FutureWarning </div>

&nbsp;

- **StackOverflow Research**: I actively sought solutions by searching through community forums like Stack Overflow. It was during this research that I learned about the FutureWarning and its implications.

- **Suppressing Warnings**: To prevent the FutureWarning messages from cluttering the output, I implemented code to suppress warnings specifically related to the Seaborn library. This allowed me to maintain a clean and informative environment for data visualization.

By addressing these challenges, I not only enhanced the robustness of the project but also gained valuable problem-solving skills that are essential in the field of data analysis and web scraping.

## Conclusion

The "E7 Hero Data" project combines web scraping, data analysis, visualization, and web development to create a comprehensive platform for exploring and understanding character data from Epic Seven. Users can interact with the data through the web dashboard, explore character statistics, and gain valuable insights into the game's characters. (Once I deploy the web-app anyways). This project showcases how data extraction, analysis, and visualization can be transformed into an engaging and informative dashboard.

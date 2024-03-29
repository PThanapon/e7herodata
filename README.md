# Project: E7 Hero Data

## Introduction

"E7 Hero Data" is a personal project which involves web scraping, data analysis, visualization, and the creation of an interactive web dashboard. This project is dedicated to extracting, analyzing, and presenting data related to characters from  Epic Seven. 

For some context, Epic Seven is a turn-based strategy game developed by a Korean game company Smilegate. In a fight, heroes take turns to use their ability to deal damage, heal or provide utility such as buffing allies and debuffing enemies. Each heroes would have a rarity from 1 to 5 Stars; though 1 and 2 stars heroes are rarely use in a fight but rather as fodders to upgrade other heroes so I have omitted them from this project. Together with Class and Horoscope, the base stats of a hero could be determined; with some exceptions such as Summertime Iseria having a 50% atk increase from her Passive skills. This project aims to display the relationships between each of the factors and explores how each stats relate to one anothers. (Side note: from the picture, you might notice that theres are "equipments" that each hero can equip. These could give either a flat or a percentage increase based on the base stat. Hence, this is why it is why it is important for a hero to have a high base stat)

![](https://cdn.discordapp.com/attachments/844184695754457122/1155190810887856138/Screenshot_20230924-011148_Epic_Seven.jpg "Summertime Iseria")

<div align="center"> Summertime Iseria, a 5 Star, Capricorn, Ranger </div>

&nbsp;

## Key Findings

1. While flat stats (Attack, Heath, Defense and Speed) and effectiveness generally increase with increasing rarity, other percentage stat (Crit Chance, Crit Damage, Eff Res) does not follow this trend. Notably, Crit Chance has the opposite relationship.

![](https://media.discordapp.net/attachments/844184695754457122/1156253852660666559/image.png?ex=65144cd0&is=6512fb50&hm=eef5ad0eac1a8cba557d2998eb0d6e4de2b7bc6b59d339dd8b3ea9dfe112ee68&=&width=1920&height=971 "flat average")

<div align="center"> Flat Stat average based on rarity </div>

&nbsp;

![](https://media.discordapp.net/attachments/844184695754457122/1156254543739359243/image.png?ex=65144d75&is=6512fbf5&hm=b11581adf81c6d625d88ab506e7a5476e80e6039cba76e8e876042375fb3272b&=&width=1920&height=971 "cc avg")

<div align="center"> Average of Crit Chance based on rarity </div>

&nbsp;

2. Different class have their own "specialities"
- Mage has high Attack, Defense, Effectiveness, medium Speed, Crit Chance, Eff Res and low Health.
- Thief has high Attack, Crit Chance, Speed, medium Health, low Defense, Effectiveness and low Eff Res
= Ranger has high Attack, Speed, Effectiveness, medium Health, Defense, Crit Chance and low Eff Res
- Warrior has high Attack, medium Health, Defense, Speed, Crit Chance and low Effectiveness and Eff Res 
- Knight has high Health, Defense, medium Attack, Crit Chance, Effectiveness, Eff Res and low Speed
- Soul Weaver has High Defense and Eff Res, medium Speed Effectiveness and low Attack, Health and Crit Chance
- Crit Damage is pretty constant for all class.

![](https://media.discordapp.net/attachments/844184695754457122/1156266090960269342/image.png?ex=65145836&is=651306b6&hm=3ba43f02292ac681519f4fbeddf1efbe11240a1a5579ed90bb2f677b3eda0b11&=&width=1920&height=338 "avg by class")

<div align="center"> Average of stats by class </div>

&nbsp;

3. Horoscopes can be extreme:
- The horoscope Cancer ranked near the top for defensive (hp, def) stat while being near the bottom for utility stat (speed, eff, er) and offensive stat (atk, cc). Similar to previously, crit damage does not really vary with horoscope.
- On the other hand, horoscope Leo ranked near the bottom for defensive stat and utility stat while being near the top for offensive stat.

![](https://media.discordapp.net/attachments/844184695754457122/1156297106974322748/cancer-horoscope.png?ex=65147519&is=65132399&hm=945ed17c93b1dfad289aa087b5223f8072cf911c6337c25e7feae955fb148a1b&=&width=1283&height=993 "avg by horoscope")

<div align="center"> Health, Defense, Attack and Speed by Horoscope (Arrow pointing to Cancer) </div>

&nbsp;

4. Correlation and Conclusion
- It should be quite clear that in Epic Seven, there are no class, horoscope and rarity which are the best for everything. In order for the game to be balanced, there should always be a tradeoff between one stat and another. To confirm the general trend and relationship between each stat, we can use plot a Correlation Matrix using Matplotlib.

![](https://media.discordapp.net/attachments/844184695754457122/1156298448006549665/correlation.png?ex=65147658&is=651324d8&hm=a479efd546059b220b8e67e5aebf1399efacb2047b137c804f72af6c55033a90&=&width=884&height=783 "avg by horoscope")

&nbsp;

- **Negative Correlations:**

    - Attack vs. Health and Defense: Characters with higher Attack tend to have slightly lower Health (-0.1554) and moderately lower Defense (-0.4165).
    - Health vs. Crit Chance and Speed: Characters with higher Health tend to have a lower chance of landing critical hits (-0.2618) and are slower (-0.2619).
    - Crit Chance vs. Defense and Effectiveness Resistance: Characters with a higher critical chance tend to have lower Defense (-0.4776) and lower Effectiveness Resistance (-0.3204).
    - Defense vs. Speed: Characters with higher Defense tend to be slower (-0.5589).

- **Positive Correlations:**

    - Attack vs. Crit Chance and Speed: Characters with higher Attack tend to have a higher chance of landing critical hits (0.2819) and are faster (0.3417).
    - Defense vs. Effectiveness Resistance: Characters with higher Defense tend to have higher Effectiveness Resistance (0.3594).
    - Crit Chance vs. Critical Damage and Speed: Characters with a higher crit chance also tend to have higher critical damage (0.2484) and be faster (0.3160).
    - Speed vs. Effectiveness: Characters with higher speed tend to have slightly higher Effectiveness (0.1968).

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
```
df = pd.read_csv('e7herodata.csv')
```

- **Data Categorization**: It establishes filters to categorize characters based on the attributes: rarity, class, and horoscope.
```
filters = {
    "rarity": [3, 4, 5],    
    "class": ["Warrior", "Knight", "Soul Weaver", "Ranger", "Mage", "Thief"],
    "horoscope": ["Aries", "Gemini", "Leo", "Sagittarius", "Libra", "Scorpio",
        "Capricorn", "Cancer", "Aquarius", "Taurus", "Pisces", "Virgo"]
}
```

- **Statistics Calculation**: Percentile values for specific character statistics such as attack, health, defense, etc based on the filters are calculated
```
perc = []
for v in range(len(temp)):
    perc.append(v * 100 / (len(temp) - 1))
```

- **Visualization**: A key feature of this script is the creation of line plots that visually demonstrate how character statistics vary across different categories.
  - We iterate through each filter and stat
```
for filt in filters:
    for stat in stats:
```
  - Which we can then create the visualization using the value of filt and stat. First we append the dictionary stats with the sorted value of the current stat based on the current filter. Then we go through the filter; for eg. filter rarity will go through rarity = 3, 4 then 5, and plot the graph together with the calculated percentile earlier as the x-axis.
```
stats[stat].append(df.sort_values(by=[stat]))

for i, fil in enumerate(filters[filt]):
temp = stats[stat][0][stats[stat][0][filt] == fil]

    perc = []
    for v in range(len(temp)):
        perc.append(v * 100 / (len(temp) - 1))

    stats[stat].append(temp)
    plt.plot(perc, stats[stat][i + 1][stat].values, colour[i], label=filters[filt][i])

plt.title(f"{stat} by {filt}")
plt.xlabel("percentile")
plt.ylabel(stat)
plt.legend()
```


&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![](https://cdn.discordapp.com/attachments/844184695754457122/1155136996247863296/image.png "Speed by class")

<div align="center"> Distribution of Speed by Class </div>

&nbsp;

- **Plot Storage**: The resulting plots are stored as png files, each depicting the variation of a specific statistic (e.g., attack) across distinct character categories (e.g., rarity) with the convention stat-filter.png
```
plt.savefig(f"{stat}-{filt}.png")
plt.clf()
```
![](https://media.discordapp.net/attachments/844184695754457122/1156248987435802765/image.png?ex=65144848&is=6512f6c8&hm=b2d83d5340ef2be5437bbf44ccd64dcd98a6ea766f1c78a0a5b7d5c1c225118e&=&width=1920&height=636 "E7 Hero Data Graphs")

<div align="center"> Here's the 24 graphs plotted with Matplotlib </div>

&nbsp;

## Part 3: Additional Data Analysis ( [e7supplementary.py](https://github.com/pthanapon/e7herodata/blob/main/e7supplementary.py) )

This section introduces the script `e7supplementary.py`, which enhances the project with additional data analysis. Here's an overview of its role:

- **Data Import**: The script imports character data from the "e7HeroData.csv" file using the Pandas library similarly to part 2.

- **Mean Calculation**: It computes the mean values for specific character statistics.
```
mean_df = df.groupby(fil)[stat].mean().reset_index()
```

- **Data Grouping**: The script groups the data based on filter criteria such as rarity, class, and horoscope.
```
sorted_df = mean_df.sort_values(by=stat)
```

- **Visualization**: For each stat, it generates a series of bar plots, one for each filter, to visualize the average value of that statistic across various categories together in a single plot.
```
for stat in stats:
    fig, axes = plt.subplots(len(filter), figsize=(8, 12))
    
    for i, fil in enumerate(filter):
        mean_df = df.groupby(fil)[stat].mean().reset_index()

        sorted_df = mean_df.sort_values(by=stat)

        sns.barplot(data=sorted_df, x=fil, y=stat, ax=axes[i])

        axes[i].set_title(f"Average {stat} by {fil}")
        axes[i].set_xlabel(fil)
        axes[i].set_ylabel(f"Average {stat}")
```

&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ![](https://media.discordapp.net/attachments/844184695754457122/1155135429071343737/image.png?width=661&height=993 "Attack Averages")

<div align="center"> Mean of Attack based on Rarity, Class and Horoscope </div>

&nbsp;

- **Plot Storage**: The resulting plots are saved as image files, each illustrating the average value of a specific statistic by category.

While Part 2 use Matplotlib for visualization, Part 3 employs the Seaborn library to create these informative visualizations.
Together, these visualizations allowing me to explore character statistics from different perspectives and gain valuable insights into the game's characters.

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

- **User Interface**: It sets up a user-friendly interface with elements like dropdown menus to select the filters, visualizations, comments for the plots and a button to download the shown image.

- **Callback Functions**: Dash callbacks are defined to handle user interactions. For example, selecting different filters or statistics updates the displayed character image, comment, and download link.

![](https://media.discordapp.net/attachments/844184695754457122/1155921908450213898/image.png?width=1075&height=572 "E7 Hero Data Dashboard")

<div align="center"> Dropdown Menu for stat options </div>

&nbsp;  

- **Deployment**: The Dash app is deployed locally through localhost and Heroku, making character data accessible and interactive via a web interface. Took Heroku app down due to monthly cost.


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

- **Suppressing Warnings**: To prevent the FutureWarning messages from cluttering the output, I implemented code to suppress warnings using the Warning module. This allowed me to maintain a clean and informative environment for data visualization.

By addressing these challenges, I not only enhanced the robustness of the project but also gained valuable problem-solving skills that are essential in the field of data analysis and web scraping.

## Conclusion

The "E7 Hero Data" project combines web scraping, data analysis, visualization, and web development to create a comprehensive platform for exploring and understanding character data from Epic Seven. Users can interact with the data through the web dashboard, explore character statistics, and gain valuable insights into the game's characters. This project showcases how data extraction, analysis, and visualization can be transformed into an engaging and informative dashboard.

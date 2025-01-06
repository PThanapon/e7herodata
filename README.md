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

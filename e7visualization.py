import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('e7herodata.csv')

colour = ["b", "g", "r", "c", "m", "y", "k", "dimgrey", "tab:brown", "tab:orange", "tab:purple", "tab:pink"]
filters = {
    "rarity": [3, 4, 5],
    "class": ["Warrior", "Knight", "Soul Weaver", "Ranger", "Mage", "Thief"],
    "horoscope": ["Aries", "Gemini", "Leo", "Sagittarius", "Libra", "Scorpio", "Capricorn", "Cancer", "Aquarius", "Taurus", "Pisces", "Virgo"]
}

for filt in filters:
    if filt != "horoscope":
        #continue
        pass

    stats = {"attack": [],
             "health": [],
             "defense": [],
             "crit chance": [],
             "crit damage": [],
             "effectiveness": [],
             "eff. res.": [],  # Shortened label
             "speed": []}

    for stat in stats:
        if stat != "attack":
            #continue
            pass

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

        plt.savefig(f"{stat}-{filt}.pdf")
        plt.clf()

        print(f"running.............. {filt}, {stat}")

    


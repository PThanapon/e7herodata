import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv("e7herodata.csv")

stats = ['attack', 'health', 'defense', 'crit chance', 'crit damage', 'effectiveness', 'effectiveness resistance', 'speed']
filter = ["rarity", "class", "horoscope"]

for stat in stats:
    fig, axes = plt.subplots(len(filter), figsize=(8, 12))
    
    for i, fil in enumerate(filter):
        mean_df = df.groupby(fil)[stat].mean().reset_index()

        sorted_df = mean_df.sort_values(by=stat)

        sns.barplot(data=sorted_df, x=fil, y=stat, ax=axes[i])

        axes[i].set_title(f"Average {stat} by {fil}")
        axes[i].set_xlabel(fil)
        axes[i].set_ylabel(f"Average {stat}")

    plt.tight_layout()
    plt.savefig(f"{stat}_averages.png")
    plt.close()

print("Plots saved as image files.")









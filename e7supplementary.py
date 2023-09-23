import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv("e7herodata.csv")

# Define the list of stats you want to calculate the mean for
stats_to_calculate = ['attack', 'health', 'defense', 'crit chance', 'crit damage', 'effectiveness', 'effectiveness resistance', 'speed']
filter_columns = ["rarity", "class", "horoscope"]

# Create one subplot per statistic
for stat in stats_to_calculate:
    fig, axes = plt.subplots(len(filter_columns), figsize=(8, 12))
    
    for i, fil in enumerate(filter_columns):
        # Calculate the mean of the current stat
        mean_df = df.groupby(fil)[stat].mean().reset_index()
        
        # Sort the DataFrame by the mean of the current stat
        sorted_df = mean_df.sort_values(by=stat)
        
        if fil == "rarity":
            # Create a sorted list of rarity values based on the mean of the current stat
            rarity_order = sorted_df[fil]
            sns.barplot(data=sorted_df, x=fil, y=stat, ax=axes[i], order=rarity_order)
        else:
            sns.barplot(data=sorted_df, x=fil, y=stat, ax=axes[i])

        axes[i].set_title(f"Average {stat} by {fil}")
        axes[i].set_xlabel(fil)
        axes[i].set_ylabel(f"Average {stat}")

    plt.tight_layout()
    plt.savefig(f"{stat}_averages.png")
    plt.close()  # Close the current figure to release memory

print("Plots saved as image files.")



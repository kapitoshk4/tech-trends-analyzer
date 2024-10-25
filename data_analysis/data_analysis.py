import os

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

from parse.config import EXPERIENCE_LEVELS

vacancies = pd.read_csv("vacancies.csv")


def plot_technology_frequency(df: pd.DataFrame, title: str, filename: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.bar(df["Technology"], df["Count"], color="skyblue")
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel("Technology")
    plt.ylabel("Number of Vacancies")
    plt.tight_layout()

    plt.savefig(filename)
    plt.show()


def count_technologies(df: pd.DataFrame) -> pd.DataFrame:
    all_technologies = df["technologies"].str.split(", ")
    flat_technologies = [tech.strip() for sublist in all_technologies for tech in sublist]
    technology_counts = Counter(flat_technologies)
    technologies_df = pd.DataFrame(technology_counts.items(), columns=["Technology", "Count"])
    return technologies_df.sort_values(by="Count", ascending=False)


base_dir = os.path.dirname(os.path.dirname(__file__))
diagrams_directory = os.path.join(base_dir, "data_analysis/diagrams")
os.makedirs(diagrams_directory, exist_ok=True)
overall_tech_df = count_technologies(vacancies)
plot_technology_frequency(
    overall_tech_df,
    "Overall Frequency of Technologies in Vacancies",
    "diagrams/technology_frequency_overall.png"
)

experience_levels = set(EXPERIENCE_LEVELS.values())

for level in experience_levels:
    df_filtered = vacancies[vacancies["experience"] == level]
    tech_df = count_technologies(df_filtered)
    plot_technology_frequency(
        tech_df, f"Frequency of Technologies in {level} Vacancies",
        f"diagrams/technology_frequency_{level.lower().replace(' ', '_')}.png"
    )

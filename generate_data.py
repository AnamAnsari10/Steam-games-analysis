"""
Generates a synthetic-but-realistic Steam games dataset for EDA practice.

Why synthetic: this environment has no internet access, so a real Kaggle
"Steam Games" dataset can't be downloaded. This script fabricates data with
realistic distributions and relationships (genre affects price/owners,
indie vs AAA effects, review-bomb outliers, etc.) so every chart in the
notebook tells a plausible, non-trivial story.

To use a REAL dataset instead: replace data/steam_games.csv with one
downloaded from Kaggle (e.g. "Steam Store Games" or "Steam Games Dataset")
that has similar columns, and the notebook will work with minimal changes.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 1200

genres = ["Action", "Indie", "Adventure", "RPG", "Strategy", "Simulation",
          "Casual", "Sports", "Racing", "Free to Play"]
genre_weights = [0.20, 0.22, 0.14, 0.12, 0.09, 0.08, 0.07, 0.04, 0.02, 0.02]

publishers = ["Valve", "Devolver Digital", "Paradox Interactive", "Team17",
              "Ubisoft", "EA", "Square Enix", "Focus Entertainment",
              "Indie Collective", "Private Division", "505 Games",
              "Annapurna Interactive", "Raw Fury", "Solo Studio"]

platforms_opts = ["windows", "windows;mac", "windows;mac;linux", "windows;linux"]

adjectives = ["Shadow", "Iron", "Crimson", "Lost", "Eternal", "Silent", "Broken",
              "Rogue", "Ashen", "Frozen", "Neon", "Void", "Dark", "Golden", "Rusty"]
nouns = ["Kingdom", "Legacy", "Odyssey", "Protocol", "Horizon", "Requiem",
         "Uprising", "Sanctuary", "Chronicles", "Descent", "Frontier", "Citadel",
         "Wanderer", "Reckoning", "Colony"]

def make_name(i):
    return f"{rng.choice(adjectives)} {rng.choice(nouns)}" + (f" {i%7+1}" if rng.random() < 0.08 else "")

rows = []
for i in range(N):
    genre = rng.choice(genres, p=genre_weights)
    is_indie = genre == "Indie" or rng.random() < 0.35
    is_free = genre == "Free to Play" or rng.random() < 0.06

    # Release date: weighted toward more recent years (Steam catalog growth)
    year = int(rng.choice(range(2008, 2026), p=np.array([0.01,0.01,0.015,0.02,0.02,0.03,0.03,
                                                           0.04,0.05,0.06,0.07,0.08,0.09,0.09,
                                                           0.10,0.10,0.09,0.05]) /
                           np.sum([0.01,0.01,0.015,0.02,0.02,0.03,0.03,0.04,0.05,0.06,0.07,
                                   0.08,0.09,0.09,0.10,0.10,0.09,0.05])))
    month = int(rng.integers(1, 13))
    day = int(rng.integers(1, 29))
    release_date = pd.Timestamp(year=year, month=month, day=day)

    # Price depends on genre & indie status
    if is_free:
        price = 0.0
    else:
        base = {"Action": 19.99, "RPG": 24.99, "Strategy": 22.99, "Simulation": 18.99,
                "Adventure": 14.99, "Casual": 6.99, "Sports": 29.99, "Racing": 19.99,
                "Indie": 9.99, "Free to Play": 0.0}[genre]
        mult = 0.5 if is_indie else rng.uniform(0.9, 1.6)
        price = round(max(0.99, base * mult * rng.uniform(0.7, 1.3)), 2)

    # Review counts: heavy-tailed, AAA/non-indie skew higher
    scale = 4000 if not is_indie else 500
    total_reviews = int(rng.pareto(1.2) * scale) + rng.integers(0, 50)
    total_reviews = min(total_reviews, 500000)

    # Positive ratio: mostly good games, some bombs, some mixed
    quality = rng.beta(6, 2)  # skewed toward positive
    if rng.random() < 0.05:
        quality = rng.beta(1.5, 6)  # a "bad game" outlier
    positive = int(total_reviews * quality)
    negative = total_reviews - positive

    # Playtime (minutes) correlated loosely with quality & genre
    genre_playtime_base = {"RPG": 3200, "Strategy": 2600, "Simulation": 2200,
                            "Action": 1400, "Adventure": 900, "Casual": 300,
                            "Sports": 1200, "Racing": 800, "Indie": 700,
                            "Free to Play": 1800}[genre]
    avg_playtime = max(5, int(rng.normal(genre_playtime_base * (0.6 + 0.8*quality), genre_playtime_base*0.4)))
    median_playtime = max(0, int(avg_playtime * rng.uniform(0.3, 0.8)))

    developer = rng.choice(publishers) if not is_indie else make_name(i) + " Studio"
    publisher = rng.choice(publishers)
    platforms = rng.choice(platforms_opts, p=[0.55, 0.2, 0.15, 0.10])

    rows.append({
        "appid": 100000 + i,
        "name": make_name(i),
        "release_date": release_date.date().isoformat(),
        "developer": developer,
        "publisher": publisher,
        "primary_genre": genre,
        "is_indie": is_indie,
        "price_usd": price,
        "positive_ratings": positive,
        "negative_ratings": negative,
        "total_ratings": total_reviews,
        "average_playtime_min": avg_playtime,
        "median_playtime_min": median_playtime,
        "platforms": platforms,
    })

df = pd.DataFrame(rows)

# Sprinkle a few realistic data-quality issues to make cleaning meaningful
dup_rows = df.sample(8, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)
missing_idx = df.sample(frac=0.03, random_state=2).index
df.loc[missing_idx, "developer"] = np.nan
missing_idx2 = df.sample(frac=0.01, random_state=3).index
df.loc[missing_idx2, "price_usd"] = np.nan

df.to_csv("/home/claude/steam_eda/data/steam_games.csv", index=False)
print(df.shape)
print(df.head())

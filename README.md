# Steam Games — EDA Project

## Structure
```
steam_eda/
├── steam_games_eda.ipynb   # Main analysis notebook — start here
├── data/
│   ├── steam_games.csv     # The dataset used by the notebook
│   └── generate_data.py    # Script that generated steam_games.csv
└── README.md
```

## About the data
`data/steam_games.csv` is a **synthetic dataset** (1,200 games) built to mimic
realistic Steam catalog patterns — price by genre, indie vs. non-indie effects,
long-tailed review counts, some review-bomb outliers, and a handful of missing
values / duplicate rows so the cleaning steps in the notebook are meaningful.

**Columns:** `appid, name, release_date, developer, publisher, primary_genre,
is_indie, price_usd, positive_ratings, negative_ratings, average_playtime_min,
median_playtime_min, platforms`

### Using a real dataset instead
1. Download a real Steam dataset, e.g. from Kaggle ("Steam Store Games" or
   "Steam Games Dataset").
2. Save it as `data/steam_games.csv`, matching the column names above (or
   update the column names in Section 1 of the notebook).
3. Re-run the notebook — everything downstream works off those column names.

## Running the notebook
```
pip install pandas numpy matplotlib seaborn jupyter
jupyter notebook steam_games_eda.ipynb
```
Then **Run All**.

## What the notebook covers:
1. Setup & data loading
2. Data overview & cleaning (missing values, duplicates)
3. Univariate analysis — price, genre, review score, playtime distributions
4. Bivariate/multivariate analysis — price by genre, indie vs. non-indie,
   price vs. rating, correlation heatmap
5. Time trends — releases per year, average price/rating over time, genre
   popularity over time
6. Top games and publishers by review count / score
7. Key takeaways template — fill in your own observations after exploring

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read dataset
df = pd.read_csv("matches.csv")

# EDA
print(df.head())
print(df.info())
print(df.describe())

print("Shape:", df.shape)
print("Columns:", df.columns)

print("Missing values:")
print(df.isna().sum())

print("Duplicate rows:", df.duplicated().sum())

# Data cleaning

# Remove duplicates
df.drop_duplicates(inplace=True)


# Remove unnecessary columns

df.drop(columns=[
   "tournament_id",
    "match_id",
    "home_team_id",
    "away_team_id",
    "score_penalties",
    "home_team_score_penalties",
    "away_team_score_penalties",
    "penalty_shootout",
    "replayed",
    "replay",
    "match_time","stadium_id"
], inplace=True)


# Remove FIFA Womens World Cup  
df = df[~df["tournament_name"].str.contains("Women's", na=False)]


# Data Analysis

# Analysis 1 :Top 10 Teams by Number of FIFA World Cup Matches

#  Number of matches as home team
home_matches = df["home_team_name"].value_counts()

# Number of matches as a guest
away_matches = df["away_team_name"].value_counts()

# Total number of matches

total_matches = home_matches.add(away_matches,fill_value=0)

# Match schedule
total_matches = total_matches.sort_values(ascending=False)

# Most participating team 
print(total_matches.head(10))

# Visualization 1: Top 10 Teams by Number of FIFA World Cup Matches
top10 = total_matches.head(10)
plt.figure(figsize=(10,6))
top10.plot(kind="bar",color="gray",lw="5")
plt.title("Top 10 Teams by Number of FIFA World Cup Matches")
plt.xlabel("Team",fontsize=15)
plt.ylabel("Number of Matches",fontsize=15)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()




# Analysis 2 :top 10 Teams FIFA World Cup Wins
home_wins = df[df["home_team_score"] > df["away_team_score"]]["home_team_name"].value_counts()

away_wins = df[df["away_team_score"] > df["home_team_score"]]["away_team_name"].value_counts()

total_wins = home_wins.add(away_wins,fill_value=0).sort_values(ascending=False)

print(total_wins.head(10))

# Visualization 2: Top 10 Teams by FIFA World Cup Wins
top10 = total_wins.head(10)
plt.figure(figsize=(10,6))
top10.plot(kind="bar",lw=5,color="black")
plt.title("Top 10 Teams by FIFA World Cup Wins",fontsize=15)
plt.xlabel("Team",fontsize=15)
plt.ylabel("Number of Matches",fontsize=15)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# Analysis 3 :top 10 Teams FIFA World Cup losses

losses_home = df[df["home_team_score"] < df["away_team_score"]]["home_team_name"].value_counts()

losses_away = df[df["away_team_score"] < df["home_team_score"]]["away_team_name"].value_counts()

total_losses = losses_home.add(losses_away,fill_value=0).sort_values(ascending=False)

print("top 10 Teams FIFA World Cup losses : ",total_losses.head(10))

# Visualization 3: Top 10 Teams by FIFA World Cup Losses
top10 = total_losses.head(10)
plt.figure(figsize=(10,6))
top10.plot(kind="bar",lw=5,color="red")
plt.title("Top 10 Teams by FIFA World Cup Losses",fontsize=15)
plt.xlabel("Team",fontsize=15)
plt.ylabel("Number of losses",fontsize=15)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Analysis 4 :top 10 Teams by Number of Draws in FIFA World Cup draws

draw_home = df[df["home_team_score"] == df["away_team_score"]]["home_team_name"].value_counts()

draw_away = df[df["away_team_score"] == df["home_team_score"]]["away_team_name"].value_counts()

total_draws = draw_home.add(draw_away,fill_value=0).sort_values(ascending=False)

print(total_draws.head(10))

# Visualization 4: Top 10 Teams by Number of Draws in FIFA World Cup Matches
top10 = total_draws.head(10)
plt.figure(figsize=(10,6))
top10.plot(kind="bar",lw=5,color="orange")
plt.title("Top 10 Teams by Number of Draws in FIFA World Cup",fontsize=15)
plt.xlabel("Team",fontsize=15)
plt.ylabel("Number of Draws",fontsize=15)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Analysis 5: Top 10 Teams by Goals Scored
home_goals=df.groupby("home_team_name")["home_team_score"].sum()
away_goals=df.groupby("away_team_name")["away_team_score"].sum()
total_goals = home_goals.add(away_goals,fill_value=0).sort_values(ascending=False)
print(total_goals.head(10))

# Visualization 5: Top 10 Goal-Scoring Teams in FIFA World Cup
top10 = total_goals.head(10)
plt.figure(figsize=(10,6))
top10.plot(kind="bar",color="purple")
plt.title("Top 10 Teams by Goals Scored in FIFA World Cup",fontsize=15)
plt.xlabel("Teams",fontsize=15)
plt.ylabel("Goals Scored",fontsize=15)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()




# Analysis 6: Average Goals per FIFA World Cup Edition

df["total_goals"] = df["home_team_score"] + df["away_team_score"]
avg_goals = df.groupby("tournament_name")["total_goals"].mean()
print(avg_goals)
# Visualization 6: Average Goals per FIFA World Cup Edition
plt.figure(figsize=(10,6))
avg_goals.plot(kind="line",marker="o",color="blue")
plt.title("Average Goals per FIFA World Cup Edition",fontsize=15)
plt.xlabel("World Cup Edition",fontsize=15)
plt.ylabel("Average Goals per Match",fontsize=15)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# Analysis 7: Total Goals in Each FIFA World Cup Edition

goals_per_edition = df.groupby("tournament_name")["total_goals"].sum().sort_values(ascending=False)
print(goals_per_edition)

# Visualization 7: Total Goals in Each FIFA World Cup Edition
plt.figure(figsize=(10,6))
goals_per_edition.plot(kind="bar")
plt.title("Total Goals in Each FIFA World Cup Edition")
plt.xticks(rotation=45)
plt.legend(
    title="World Cup Edition",
    loc="center left",
    bbox_to_anchor=(1.30, 0.5)
)
plt.show()




# Data for Streamlit

analysis_data = {
    "total_matches": len(df),

    "total_goals": int(df["total_goals"].sum()),

    "average_goals": round(df["total_goals"].mean(), 2),

    "number_of_teams": len(
        set(df["home_team_name"].dropna()) |
        set(df["away_team_name"].dropna())
    ),

    "total_matches_by_team": total_matches,

    "total_wins": total_wins,

    "total_losses": total_losses,

    "total_draws": total_draws,

    "total_goals_by_team": total_goals,

    "avg_goals_by_edition": avg_goals,

    "goals_per_edition": goals_per_edition
}
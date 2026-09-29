import streamlit as st
import pandas as pd
import analysis
import matplotlib.pyplot as plt

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="FIFA World Cup Analysis",
    page_icon="⚽",
    layout="wide"
)

# ==========================================
# Title
# ==========================================

st.title("⚽ FIFA World Cup Analysis Dashboard")

st.markdown(
    """
    Interactive dashboard for analyzing FIFA World Cup matches,
    teams, goals, wins, losses, and draws.
    """
)

# ==========================================
# Load data from analysis.py
# ==========================================

df = analysis.df
data = analysis.analysis_data

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("⚙️ Dashboard Controls")

analysis_option = st.sidebar.selectbox(
    "Choose Analysis",
    [
        "Overview",
        "Team Analysis",
        "Top Teams by Matches",
        "Top Teams by Wins",
        "Top Teams by Losses",
        "Top Teams by Draws",
        "Top Teams by Goals",
        "Average Goals per World Cup",
        "Total Goals per World Cup"
    ]
)

# ==========================================
# Overview
# ==========================================

if analysis_option == "Overview":

    st.header("📊 World Cup Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Matches",
        data["total_matches"]
    )

    col2.metric(
        "Total Goals",
        data["total_goals"]
    )

    col3.metric(
        "Average Goals / Match",
        data["average_goals"]
    )

    col4.metric(
        "Number of Teams",
        data["number_of_teams"]
    )

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# ==========================================
# Team Analysis
# ==========================================

elif analysis_option == "Team Analysis":

    st.header("⚽ Team Analysis")

    # Get all teams
    teams = sorted(
        set(df["home_team_name"].dropna()) |
        set(df["away_team_name"].dropna())
    )

    # Team selector
    selected_team = st.selectbox(
        "Select a Team",
        teams
    )

    # ======================================
    # Filter matches for selected team
    # ======================================

    team_matches = df[
        (df["home_team_name"] == selected_team) |
        (df["away_team_name"] == selected_team)
    ].copy()

    # ======================================
    # Matches
    # ======================================

    total_matches = len(team_matches)

    # ======================================
    # Wins
    # ======================================

    wins = (
        (
            (team_matches["home_team_name"] == selected_team) &
            (team_matches["home_team_score"] > team_matches["away_team_score"])
        )
        |
        (
            (team_matches["away_team_name"] == selected_team) &
            (team_matches["away_team_score"] > team_matches["home_team_score"])
        )
    ).sum()

    # ======================================
    # Losses
    # ======================================

    losses = (
        (
            (team_matches["home_team_name"] == selected_team) &
            (team_matches["home_team_score"] < team_matches["away_team_score"])
        )
        |
        (
            (team_matches["away_team_name"] == selected_team) &
            (team_matches["away_team_score"] < team_matches["home_team_score"])
        )
    ).sum()

    # ======================================
    # Draws
    # ======================================

    draws = (
        team_matches["home_team_score"] ==
        team_matches["away_team_score"]
    ).sum()

    # ======================================
    # Goals Scored
    # ======================================

    goals_scored = (
        team_matches.loc[
            team_matches["home_team_name"] == selected_team,
            "home_team_score"
        ].sum()
        +
        team_matches.loc[
            team_matches["away_team_name"] == selected_team,
            "away_team_score"
        ].sum()
    )

    # ======================================
    # Goals Conceded
    # ======================================

    goals_conceded = (
        team_matches.loc[
            team_matches["home_team_name"] == selected_team,
            "away_team_score"
        ].sum()
        +
        team_matches.loc[
            team_matches["away_team_name"] == selected_team,
            "home_team_score"
        ].sum()
    )

    # ======================================
    # Win Rate
    # ======================================

    if total_matches > 0:
        win_rate = (wins / total_matches) * 100
    else:
        win_rate = 0

    # ======================================
    # Display Team Name
    # ======================================

    st.subheader(f"🏆 {selected_team}")

    # ======================================
    # Statistics
    # ======================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Matches",
        total_matches
    )

    col2.metric(
        "Wins",
        int(wins)
    )

    col3.metric(
        "Losses",
        int(losses)
    )

    col4.metric(
        "Draws",
        int(draws)
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Goals Scored",
        int(goals_scored)
    )

    col2.metric(
        "Goals Conceded",
        int(goals_conceded)
    )

    col3.metric(
        "Win Rate",
        f"{win_rate:.2f}%"
    )

    col4.metric(
        "Goal Difference",
        int(goals_scored - goals_conceded)
    )

    st.divider()

    # ======================================
    # Team Matches
    # ======================================

    st.subheader("📋 World Cup Matches")

    display_columns = [
        "tournament_name",
        "home_team_name",
        "away_team_name",
        "home_team_score",
        "away_team_score"
    ]

    available_columns = [
        col for col in display_columns
        if col in team_matches.columns
    ]

    st.dataframe(
        team_matches[available_columns],
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # Goals Chart
    # ======================================

    st.subheader("⚽ Goals Analysis")

    goals_data = pd.DataFrame({
        "Goals": [
            goals_scored,
            goals_conceded
        ]
    }, index=[
        "Goals Scored",
        "Goals Conceded"
    ])

    st.bar_chart(goals_data)

# ==========================================
# Top Teams by Matches
# ==========================================

elif analysis_option == "Top Teams by Matches":

    st.header("🏆 Top 10 Teams by Number of Matches")

    top10 = data["total_matches_by_team"].head(10)

    st.bar_chart(top10)

    st.subheader("Data")

    st.dataframe(
        top10.rename("Matches"),
        use_container_width=True
    )

# ==========================================
# Top Teams by Wins
# ==========================================

elif analysis_option == "Top Teams by Wins":

    st.header("🏆 Top 10 Teams by World Cup Wins")

    top10 = data["total_wins"].head(10)

    st.bar_chart(top10)

    st.subheader("Data")

    st.dataframe(
        top10.rename("Wins"),
        use_container_width=True
    )

# ==========================================
# Top Teams by Losses
# ==========================================

elif analysis_option == "Top Teams by Losses":

    st.header("📉 Top 10 Teams by World Cup Losses")

    top10 = data["total_losses"].head(10)

    st.bar_chart(top10)

    st.subheader("Data")

    st.dataframe(
        top10.rename("Losses"),
        use_container_width=True
    )

# ==========================================
# Top Teams by Draws
# ==========================================

elif analysis_option == "Top Teams by Draws":

    st.header("🤝 Top 10 Teams by World Cup Draws")

    top10 = data["total_draws"].head(10)

    st.bar_chart(top10)

    st.subheader("Data")

    st.dataframe(
        top10.rename("Draws"),
        use_container_width=True
    )

# ==========================================
# Top Teams by Goals
# ==========================================

elif analysis_option == "Top Teams by Goals":

    st.header("⚽ Top 10 Goal-Scoring Teams")

    top10 = data["total_goals_by_team"].head(10)

    st.bar_chart(top10)

    st.subheader("Data")

    st.dataframe(
        top10.rename("Goals"),
        use_container_width=True
    )

# ==========================================
# Average Goals per World Cup
# ==========================================

elif analysis_option == "Average Goals per World Cup":

    st.header("📈 Average Goals per World Cup")

    avg_goals = data["avg_goals_by_edition"]

    st.line_chart(avg_goals)

    st.subheader("Data")

    st.dataframe(
        avg_goals.rename("Average Goals per Match"),
        use_container_width=True
    )

# ==========================================
# Total Goals per World Cup
# ==========================================

elif analysis_option == "Total Goals per World Cup":

    st.header("⚽ Total Goals per World Cup Edition")

    goals = data["goals_per_edition"]

    st.bar_chart(goals)

    st.subheader("Data")

    st.dataframe(
        goals.rename("Total Goals"),
        use_container_width=True
    )


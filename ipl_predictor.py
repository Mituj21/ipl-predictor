
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("Cricket_data.csv")
    df = df[df['home_team'].notna() & df['away_team'].notna()]
    df = df[df['home_team'] != 'TBA']
    df = df[df['away_team'] != 'TBA']
    return df

df = load_data()
team_stats = df['winner'].value_counts().to_dict()


def get_team_strength(team):
    return team_stats.get(team, 10)

def predict_match(home, away, toss_winner, toss_decision):
    home_strength = get_team_strength(home)
    away_strength = get_team_strength(away)
    toss_bonus = 2 if toss_winner == home and toss_decision.lower() == 'bat first' else 0
    home_bonus = 1
    home_score = home_strength + toss_bonus + home_bonus
    away_score = away_strength
    total = home_score + away_score
    home_prob = round((home_score / total) * 100, 2)
    away_prob = 100 - home_prob
    winner = home if home_prob > away_prob else away
    return winner, home_prob, away_prob

st.title("🏏 IPL Match Predictor")
teams = sorted(df['home_team'].dropna().unique())
home = st.selectbox("Select Home Team", teams)
away = st.selectbox("Select Away Team", [t for t in teams if t != home])
toss_winner = st.selectbox("Who Won the Toss?", [home, away])
toss_decision = st.selectbox("Toss Decision", ["Bat First", "Bowl First"])

if st.button("Predict"):
    winner, h_prob, a_prob = predict_match(home, away, toss_winner, toss_decision)
    st.markdown(f"### 🔮 Predicted Winner: **{winner}**")
    st.markdown(f"- {home} Win Chance: **{h_prob}%**")
    st.markdown(f"- {away} Win Chance: **{a_prob}%**")

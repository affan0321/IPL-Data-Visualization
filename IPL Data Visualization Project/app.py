import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="IPL Data Analysis", layout="wide")

st.title("🏏 IPL Data Analysis Dashboard")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("IPL.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("Dashboard Filters")
teams = st.sidebar.multiselect(
    "Select Teams",
    options=df['match_winner'].unique(),
    default=df['match_winner'].unique()
)

filtered_df = df[df['match_winner'].isin(teams)]

# -----------------------
# 1️⃣ Most Matches Won
# -----------------------
st.subheader("🏆 Most Matches Won By A Team")

match_wins = filtered_df['match_winner'].value_counts().reset_index()
match_wins.columns = ['Team', 'Wins']

fig1 = px.bar(
    match_wins,
    x='Wins',
    y='Team',
    orientation='h',
    color='Wins',
    color_continuous_scale='viridis'
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------
# 2️⃣ Toss Decision Trends
# -----------------------
st.subheader("🪙 Toss Decision Trends")

fig2 = px.histogram(
    df,
    x='toss_decision',
    color='toss_decision',
    title="Toss Decision Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# 3️⃣ Toss Winner vs Match Winner
# -----------------------
st.subheader("📊 Toss Winner Impact")

count = df[df['toss_winner'] == df['match_winner']]['match_id'].count()
percentage = round((count * 100) / df.shape[0], 2)

st.metric("Toss Winner Also Won Match (%)", f"{percentage}%")

# -----------------------
# 4️⃣ Matches Won By (Runs/Wickets)
# -----------------------
st.subheader("⚔ Matches Won By")

fig3 = px.histogram(
    df,
    x='won_by',
    color='won_by'
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# 5️⃣ Top 10 Players with Most POTM
# -----------------------
st.subheader("🌟 Top 10 Players With Most Player of the Match")

top_players = df['player_of_the_match'].value_counts().head(10).reset_index()
top_players.columns = ['Player', 'Awards']
fig4 = px.bar(
    top_players,
    x='Awards',
    y='Player',
    orientation='h',
    color='Awards',
    color_continuous_scale='viridis'
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------
# 6️⃣ Highest Scorers
# -----------------------
st.subheader("🔥 Top 2 Highest Scorers (Total Runs)")

high = df.groupby('top_scorer')['highscore'].sum().sort_values(ascending=False).head(2).reset_index()

fig5 = px.bar(
    high,
    x='highscore',
    y='top_scorer',
    orientation='h',
    color='highscore'
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------
# 7️⃣ Top Bowlers
# -----------------------
st.subheader("🎯 Top 10 Bowlers by Total Wickets")

df['highest_wickets'] = df['best_bowling_figure'].apply(lambda x: int(x.split('--')[0]))

top_bowlers = df.groupby('best_bowling')['highest_wickets'].sum().sort_values(ascending=False).head(10).reset_index()

fig6 = px.bar(
    top_bowlers,
    x='highest_wickets',
    y='best_bowling',
    orientation='h',
    color='highest_wickets'
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------
# 8️⃣ Venue Distribution
# -----------------------
st.subheader("🏟 Matches Played Per Venue")

venue_count = df['venue'].value_counts().reset_index()
venue_count.columns = ['Venue', 'Matches']

fig7 = px.bar(
    venue_count,
    x='Matches',
    y='Venue',
    orientation='h',
    color='Matches'
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------
# 9️⃣ Biggest Win By Runs
# -----------------------
st.subheader("🚀 Biggest Win By Runs")

big_win = df[df['won_by'] == 'Runs'].sort_values(by='margin', ascending=False).head(1)

st.write(big_win[['match_winner', 'margin']])

# -----------------------
# 🔟 Highest Individual Score
# -----------------------
st.subheader("💥 Highest Individual Score")

highest_score = df[df['highscore'] == df['highscore'].max()]
st.write(highest_score[['top_scorer', 'highscore']])

# -----------------------
# 🏁 Best Bowling Figure
# -----------------------
st.subheader("🔥 Best Bowling Figure")

best_bowling = df[df['highest_wickets'] == df['highest_wickets'].max()]
st.write(best_bowling[['best_bowling', 'best_bowling_figure']])

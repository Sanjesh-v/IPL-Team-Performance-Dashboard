import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IPL Dashboard",
    layout="wide"
)

st.title("🏏 IPL Team Performance Dashboard")
matches = pd.read_csv("data/matches.csv")

teams = sorted(
    matches['winner']
    .dropna()
    .unique()
)

team = st.sidebar.selectbox(
    "Select Team",
    teams
)

def matches_played(matches, team):

    return len(
        matches[
            (matches['team1'] == team)
            |
            (matches['team2'] == team)
        ]
    )

def total_wins(matches, team):

    return len(
        matches[
            matches['winner'] == team
        ]
    )

def win_percentage(matches, team):

    played = matches_played(
        matches,
        team
    )

    wins = total_wins(
        matches,
        team
    )

    return round(
        (wins / played) * 100,
        2
    )

played = matches_played(matches, team)
wins = total_wins(matches, team)
win_pct = win_percentage(matches, team)
losses = played - wins

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches Played",
    played
)

col2.metric(
    "Wins",
    wins
)

col3.metric(
    "Losses",
    losses
)

col4.metric(
    "Win %",
    win_pct
)

team_wins = matches[
    matches['winner'] == team
]

season_wins = (
    team_wins
    .groupby('season')
    .size()
)

st.subheader("Season-wise Wins")

st.write(season_wins)
st.line_chart(season_wins)

best_season = season_wins.idxmax()

max_wins = season_wins.max()
st.success(
    f"Best Season: {best_season} ({max_wins} wins)"
)

team_wins = matches[
    matches['winner'] == team
]

venue_wins = (
    team_wins
    .groupby('venue')
    .size()
    .sort_values(
        ascending=False
    )
)
st.subheader(
    "Venue Performance"
)

st.write(
    venue_wins.head(10)
)

st.bar_chart(
    venue_wins.head(10)
)
best_venue = venue_wins.idxmax()

venue_wins_count = venue_wins.max()
st.success(
    f"Best Venue: {best_venue} ({venue_wins_count} wins)"
)

teams = sorted(matches['winner'].dropna().unique())

team1 = st.selectbox(
    "Select Team 1",
    teams
)

team2 = st.selectbox(
    "Select Team 2",
    teams
)

h2h = matches[
    (
        (matches['team1'] == team1)
        &
        (matches['team2'] == team2)
    )
    |
    (
        (matches['team1'] == team2)
        &
        (matches['team2'] == team1)
    )
]

h2h_wins = h2h['winner'].value_counts()
st.subheader("Head-to-Head Record")

st.write(h2h_wins)
st.bar_chart(h2h_wins)

dominant_team = h2h_wins.idxmax()

dominant_wins = h2h_wins.max()
st.success(
    f"{dominant_team} leads this rivalry with {dominant_wins} wins"
)
total_matches = len(h2h)

st.metric(
    "Total Matches",
    total_matches
)

matches['toss_helped'] = (
    matches['toss_winner']
    ==
    matches['winner']
)
toss_impact = (
    matches['toss_helped']
    .mean()
    * 100
)
st.subheader("Toss Impact")

st.metric(
    "Matches Won By Toss Winner (%)",
    round(toss_impact, 2)
)

toss_wins = len(
    matches[
        matches['toss_helped']
    ]
)

total_matches=len(matches)
st.write(
    f"{toss_wins} out of {total_matches} matches were won by the toss winner."
)

deliveries = pd.read_csv(
    "data/deliveries.csv"
)

batsman_runs = (
    deliveries
    .groupby('batsman')
    ['batsman_runs']
    .sum()
)
batsman_runs = (
    batsman_runs
    .sort_values(
        ascending=False
    )
)

st.subheader(
    "Top Run Scorers"
)

st.write(
    batsman_runs.head(10)
)

top_batsman = (
    batsman_runs
    .idxmax()
)

top_runs = (
    batsman_runs
    .max()
)
st.success(
    f"Highest Run Scorer: {top_batsman} ({top_runs} runs)"
)

runs = (
    deliveries
    .groupby('batsman')
    ['batsman_runs']
    .sum()
)

balls = (
    deliveries
    .groupby('batsman')
    .size()
)

batting_stats = pd.DataFrame({
    'runs': runs,
    'balls': balls
})

batting_stats['strike_rate'] = (
    batting_stats['runs']
    /
    batting_stats['balls']
) * 100

batting_stats = batting_stats[
    batting_stats['balls'] >= 500
]
fastest_batter = (
    batting_stats['strike_rate']
    .idxmax()
)

highest_sr = (
    batting_stats['strike_rate']
    .max()
)

st.success(
    f"Highest Strike Rate: {fastest_batter} ({highest_sr:.2f})"
)

wickets = deliveries[
    deliveries['player_dismissed']
    .notna()
]

bowler_wickets = (
    wickets
    .groupby('bowler')
    .size()
    .sort_values(
        ascending=False
    )
)
st.subheader(
    "Top Wicket Takers"
)

st.write(
    bowler_wickets.head(10)
)

st.bar_chart(
    bowler_wickets.head(10)
)
bowler_runs = (
    deliveries
    .groupby('bowler')
    ['total_runs']
    .sum()
)
balls_bowled = (
    deliveries
    .groupby('bowler')
    .size()
)

bowling_stats = pd.DataFrame({
    'runs': bowler_runs,
    'balls': balls_bowled
})

overs = balls / 6

bowling_stats['overs'] = (
    bowling_stats['balls'] / 6
)

bowling_stats['economy'] = (
    bowling_stats['runs']
    /
    bowling_stats['overs']
)

bowling_stats = bowling_stats[
    bowling_stats['balls'] >= 300
]

best_economy_bowler = (
    bowling_stats['economy']
    .idxmin()
)

best_economy = (
    bowling_stats['economy']
    .min()
)
st.success(
    f"Lowest Economy: {best_economy_bowler} ({best_economy:.2f})"
)

runs = (
    deliveries
    .groupby('batsman')
    ['batsman_runs']
    .sum()
)

dismissals = (
    deliveries[
        deliveries['player_dismissed']
        .notna()
    ]
    .groupby('player_dismissed')
    .size()
)

batting_average_df = pd.DataFrame({
    'runs': runs,
    'dismissals': dismissals
})

batting_average_df = (
    batting_average_df
    .fillna(0)
)

batting_average_df = (
    batting_average_df[
        batting_average_df[
            'dismissals'
        ] > 0
    ]
)

batting_average_df[
    'average'
] = (
    batting_average_df[
        'runs'
    ]
    /
    batting_average_df[
        'dismissals'
    ]
)

batting_average_df = (
    batting_average_df[
        batting_average_df[
            'runs'
        ] >= 1000
    ]
)

best_average_batter = (
    batting_average_df[
        'average'
    ]
    .idxmax()
)

best_average = (
    batting_average_df[
        'average'
    ]
    .max()
)

st.success(
    f"Best Average: {best_average_batter} ({best_average:.2f})"
)
boundaries = deliveries[
    deliveries['batsman_runs']
    .isin([4, 6])
]

boundary_runs = (
    boundaries
    .groupby('batsman')
    ['batsman_runs']
    .sum()
)

boundary_df = pd.DataFrame({
    'total_runs': runs,
    'boundary_runs': boundary_runs
})

boundary_df = (
    boundary_df
    .fillna(0)
)

boundary_df[
    'boundary_percentage'
] = (
    boundary_df[
        'boundary_runs'
    ]
    /
    boundary_df[
        'total_runs'
    ]
) * 100

boundary_df = (
    boundary_df[
        boundary_df[
            'total_runs'
        ] >= 1000
    ]
)

most_aggressive = (
    boundary_df[
        'boundary_percentage'
    ]
    .idxmax()
)

highest_boundary_pct = (
    boundary_df[
        'boundary_percentage'
    ]
    .max()
)

st.success(
    f"Most Aggressive Batter: {most_aggressive} ({highest_boundary_pct:.2f}%)"
)

dot_balls = deliveries[
    deliveries['total_runs'] == 0
]

dot_ball_counts = (
    dot_balls
    .groupby('bowler')
    .size()
)

total_balls = (
    deliveries
    .groupby('bowler')
    .size()
)

dot_ball_df = pd.DataFrame({
    'dot_balls': dot_ball_counts,
    'total_balls': total_balls
})

dot_ball_df = (
    dot_ball_df
    .fillna(0)
)

dot_ball_df[
    'dot_ball_percentage'
] = (
    dot_ball_df[
        'dot_balls'
    ]
    /
    dot_ball_df[
        'total_balls'
    ]
) * 100

dot_ball_df = (
    dot_ball_df[
        dot_ball_df[
            'total_balls'
        ] >= 300
    ]
)

best_dot_bowler = (
    dot_ball_df[
        'dot_ball_percentage'
    ]
    .idxmax()
)

best_dot_pct = (
    dot_ball_df[
        'dot_ball_percentage'
    ]
    .max()
)

st.success(
    f"Best Dot Bowler: {best_dot_bowler} ({best_dot_pct:.2f}%)"
)


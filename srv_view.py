import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Football Player Dashboard",
    layout="wide"
)

st.title("Football Player Analytics Dashboard")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("API Sports Key", value="", type="password")
player_id = st.sidebar.text_input("Player ID", value="154")
season = st.sidebar.text_input("Season", value="2022")

fetch_button = st.sidebar.button("Fetch Data", type="primary")

if fetch_button:
    if not api_key:
        st.warning("Please enter your API Key in the sidebar.")
    else:
        url = "https://v3.football.api-sports.io/players"
        headers = {"x-apisports-key": api_key}
        querystring = {"id": player_id, "season": season}

        with st.spinner("Fetching data from API-Sports..."):
            try:
                response = requests.get(url, headers=headers, params=querystring)
                data = response.json()
            except Exception as e:
                st.error(f"Failed to reach API: {e}")
                data = {}

        if data.get("errors") and len(data["errors"]) > 0:
            st.error(f"API Error: {data['errors']}")
        elif not data.get("response"):
            st.warning("Query succeeded, but no data was returned. Check Player ID or Season.")
        else:
            player_data = data["response"][0]
            p = player_data["player"]
            stats_list = player_data["statistics"]

            st.markdown(f"## {p.get('firstname', '')} {p.get('lastname', '')} ({p.get('name', '')})")
            
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Player ID", p.get('id'))
            c2.metric("Nationality", p.get('nationality'))
            c3.metric("Age", p.get('age'))
            c4.metric("Height / Weight", f"{p.get('height', 'N/A')} | {p.get('weight', 'N/A')}")
            c5.metric("Injured", "Yes" if p.get('injured') else "No")

            st.divider()

            st.subheader("Competition Statistics")

            tab_titles = [f"{s['league']['name']} ({s['team']['name']})" for s in stats_list]
            
            if tab_titles:
                tabs = st.tabs(tab_titles)

                for idx, stat in enumerate(stats_list):
                    with tabs[idx]:
                        league = stat['league']
                        team = stat['team']
                        games = stat.get('games', {})
                        goals = stat.get('goals', {})
                        shots = stat.get('shots', {})
                        passes = stat.get('passes', {})
                        tackles = stat.get('tackles', {})
                        dribbles = stat.get('dribbles', {})
                        fouls = stat.get('fouls', {})
                        cards = stat.get('cards', {})
                        penalty = stat.get('penalty', {})

                        st.caption(f"Playing for **{team['name']}** in **{league['name']}** ({league.get('country', 'N/A')})")

                        m1, m2, m3, m4, m5 = st.columns(5)
                        m1.metric("Appearances", games.get('appearences') or 0)
                        m2.metric("Lineups", games.get('lineups') or 0)
                        m3.metric("Minutes Played", games.get('minutes') or 0)
                        m4.metric("Position", games.get('position') or 'N/A')
                        m5.metric("Rating", games.get('rating') or 'N/A')

                        st.markdown("---")

                        col_left, col_right = st.columns(2)

                        with col_left:
                            st.markdown("### Attacking Output")
                            df_attack = pd.DataFrame({
                                "Metric": ["Total Goals", "Assists", "Total Shots", "Shots on Target", "Penalties Scored", "Penalties Missed"],
                                "Count": [
                                    goals.get('total') or 0,
                                    goals.get('assists') or 0,
                                    shots.get('total') or 0,
                                    shots.get('on') or 0,
                                    penalty.get('scored') or 0,
                                    penalty.get('missed') or 0
                                ]
                            })
                            st.dataframe(df_attack, hide_index=True, use_container_width=True)

                            st.markdown("### Passing & Dribbling")
                            df_pass_dribble = pd.DataFrame({
                                "Metric": ["Total Passes", "Key Passes", "Pass Accuracy", "Dribble Attempts", "Successful Dribbles"],
                                "Value": [
                                    passes.get('total') or 0,
                                    passes.get('key') or 0,
                                    f"{passes.get('accuracy') or 0}%",
                                    dribbles.get('attempts') or 0,
                                    dribbles.get('success') or 0
                                ]
                            })
                            st.dataframe(df_pass_dribble, hide_index=True, use_container_width=True)

                        with col_right:
                            st.markdown("### Defensive Output")
                            df_defense = pd.DataFrame({
                                "Metric": ["Total Tackles", "Interceptions", "Blocks"],
                                "Count": [
                                    tackles.get('total') or 0,
                                    tackles.get('interceptions') or 0,
                                    tackles.get('blocks') or 0
                                ]
                            })
                            st.dataframe(df_defense, hide_index=True, use_container_width=True)

                            st.markdown("### Discipline & Physicality")
                            df_discipline = pd.DataFrame({
                                "Metric": ["Fouls Committed", "Fouls Drawn", "Yellow Cards", "Yellow-Red Cards", "Red Cards"],
                                "Count": [
                                    fouls.get('committed') or 0,
                                    fouls.get('drawn') or 0,
                                    cards.get('yellow') or 0,
                                    cards.get('yellowred') or 0,
                                    cards.get('red') or 0
                                ]
                            })
                            st.dataframe(df_discipline, hide_index=True, use_container_width=True)
else:
    st.info("Enter your API Key in the sidebar and click Fetch Data")

import requests

url = "https://v3.football.api-sports.io/players"

headers = {
    "x-apisports-key": " "       # Enter Your API here!
}

querystring = {
    "id": " ",       # Enter Your Player ID Here!              
    "season": " "    # Enter The Season You Want To Look For!
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

if data.get("errors"):
    print("API CHUDE JAWAR KARON:", data["errors"])
elif not data.get("response"):
    print("Query success but sessionid/playerid/season chude gesee abr check de")
else:
    player_data = data["response"][0]
    p = player_data["player"]

    print("="*55)
    print(f"PLAYER PROFILE: {p['firstname']} {p['lastname']} ({p['name']})")
    print("="*55)
    print(f"ID:             {p['id']}")
    print(f"AGE:            {p['age']}")
    print(f"Birth:          {p['birth']['date']} in {p['birth']['place']}, {p['birth']['country']}")
    print(f"Nationality:    {p['nationality']}")
    print(f"Physique:       {p['height']} | {p['weight']}")
    print(f"Ahoto:          {'HO' if p['injured'] else 'NA'}")
    print("\n" + "="*55)
    print("ONEK DETAILS ASHTESE NICHE, PANT SHAMLAO")
    print("="*55)

    for stat in player_data["statistics"]:
        team = stat['team']['name']
        league = stat['league']['name']
        country = stat['league']['country']
        games = stat['games']
        goals = stat['goals']
        shots = stat['shots']
        passes = stat['passes']
        tackles = stat['tackles']
        duels = stat['duels']
        dribbles = stat['dribbles']
        fouls = stat['fouls']
        cards = stat['cards']
        penalty = stat['penalty']

        print(f"\n {league} ({country}) - Playing for {team}")
        print("-" * 55)
        print(">> APPEARANCES & RATINGS")
        print(f"    Apps: {games.get('appearances') or 0} | Stats: {games['lineups'] or 0} | Mins: {games['minutes'] or 0}")
        print(f"    Position: {games['position']} | Rating: {games['rating'] or 'N/A'}")
        print(">> ATTA KING")
        print(f"    Goals: {goals['total'] or 0} | Assists: {['assists'] or 0}")
        print(f"    Shots Total: {shots['total'] or 0} | On Target: {shots['on'] or 0}")
        print(f"    Penalties Scored: {penalty['scored'] or 0} | Missed: {penalty['missed'] or 0}")
        print(">> PASHING & DRIB LES")
        print(f"    Total Passes: {passes['total']or 0} | Key Passes: {passes['key']or 0} | Accuracy {passes['accuracy'] or 0}%")
        print(f"    Attempts: {dribbles['attempts'] or 0} | Successful: {dribbles['success']}")
        print(">> DEFENSE SECTOR & DUEL")
        print(f"    Duels Total: {duels['total'] or 0} | Duels Won: {duels['won'] or 0}")
        print(f"    Tackles: {tackles['total'] or 0} | Interceptions: {tackles['interceptions'] or 0} | Blocks: {tackles['blocks'] or 0}")
        print(">> DC PLEEN")
        print(f"    Fouls Committed: {fouls['committed'] or 0} | Fouls Drawn: {fouls['drawn'] or 0}")
        print(f"    Yellow Cards:   {cards['yellow'] or 0} | Yellow-Red Cards: {cards['yellowred'] or 0} | Red Cards: {cards['red'] or 0}")
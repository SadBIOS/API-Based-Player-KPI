import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

PLAYER_ID = "154"
SEASON = "2022"
API_KEY = "please put the key inside me daddy"

url = "https://v3.football.api-sports.io/players"
headers = {"x-apisports-key": API_KEY}
querystring = {"id": PLAYER_ID, "season": SEASON}

console = Console()

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

if data.get("errors"):
    console.print(Panel(f"[bold red]API CHUDE JAWAR KARON:[/bold red] {data['errors']}", title="Error"))
elif not data.get("response"):
    console.print(Panel("[bold yellow]Query success but sessionid/playerid/season chude gesee abr check de[/bold yellow]", title="Warning"))
else:
    player_data = data["response"][0]
    p = player_data["player"]
    
    profile_table = Table(show_header=False, box=None)
    profile_table.add_row("[bold cyan]ID:[/bold cyan]", str(p['id']), "[bold cyan]Nationality:[/bold cyan]", p['nationality'])
    profile_table.add_row("[bold cyan]Age:[/bold cyan]", str(p['age']), "[bold cyan]Physique:[/bold cyan]", f"{p['height']} | {p['weight']}")
    profile_table.add_row("[bold cyan]Birth:[/bold cyan]", f"{p['birth']['date']} in {p['birth']['place']}, {p['birth']['country']}", "[bold cyan]Ahoto:[/bold cyan]", "[red]HO[/red]" if p['injured'] else "[green]NA[/green]")
    
    console.print(Panel(profile_table, title=f"[bold gold1]PLAYER PROFILE: {p['firstname']} {p['lastname']} ({p['name']})[/bold gold1]", border_style="gold1"))
    console.print("[bold magenta]ONEK DETAILS ASHTESE NICHE, PANT SHAMLAO[/bold magenta]\n", justify="center")

    animations = []

    for stat in player_data["statistics"]:
        team = stat['team']['name']
        league = stat['league']['name']
        country = stat['league']['country']
        games = stat['games']
        goals = stat['goals']
        shots = stat['shots']
        passes = stat['passes']
        tackles = stat['tackles']
        dribbles = stat['dribbles']
        fouls = stat['fouls']
        cards = stat['cards']
        penalty = stat['penalty']

        stat_table = Table(title=f"[bold bright_white]{league} ({country}) - Playing for {team}[/bold bright_white]", show_lines=True, header_style="bold cyan")
        stat_table.add_column("Category", style="cyan", no_wrap=True)
        stat_table.add_column("Metrics", style="white")

        stat_table.add_row("Appearances & Ratings", f"Apps: {games.get('appearences') or 0} | Lineups: {games.get('lineups') or 0} | Mins: {games.get('minutes') or 0}\nPosition: {games.get('position')} | Rating: {games.get('rating') or 'N/A'}")
        stat_table.add_row("Attacking", f"Goals: {goals.get('total') or 0} | Assists: {goals.get('assists') or 0}\nShots Total: {shots.get('total') or 0} | On Target: {shots.get('on') or 0}\nPenalties Scored: {penalty.get('scored') or 0} | Missed: {penalty.get('missed') or 0}")
        stat_table.add_row("Passing & Dribbles", f"Total Passes: {passes.get('total') or 0} | Key Passes: {passes.get('key') or 0} | Accuracy {passes.get('accuracy') or 0}%\nAttempts: {dribbles.get('attempts') or 0} | Successful: {dribbles.get('success') or 0}")
        stat_table.add_row("Defense Sector", f"Tackles: {tackles.get('total') or 0} | Interceptions: {tackles.get('interceptions') or 0} | Blocks: {tackles.get('blocks') or 0}")
        stat_table.add_row("Discipline", f"Fouls Committed: {fouls.get('committed') or 0} | Fouls Drawn: {fouls.get('drawn') or 0}\nYellow: {cards.get('yellow') or 0} | Yellow-Red: {cards.get('yellowred') or 0} | Red: {cards.get('red') or 0}")
        
        console.print(stat_table)

        df_attack = pd.DataFrame({
            'Metric': ['Total Shots', 'Shots on Target', 'Total Goals', 'Assists'],
            'Value': [shots.get('total') or 0, shots.get('on') or 0, goals.get('total') or 0, goals.get('assists') or 0]
        })
        
        d_success = dribbles.get('success') or 0
        d_fail = (dribbles.get('attempts') or 0) - d_success
        df_dribble = pd.DataFrame({
            'Metric': ['Successful', 'Unsuccessful'],
            'Value': [d_success, d_fail]
        })
        
        p_key = passes.get('key') or 0
        p_other = (passes.get('total') or 0) - p_key
        df_pass = pd.DataFrame({
            'Metric': ['Key Passes', 'Other Passes'],
            'Value': [p_key, p_other]
        })
        
        df_disc = pd.DataFrame({
            'Metric': ['Fouls Drawn', 'Fouls Committed', 'Yellow Cards', 'Red Cards'],
            'Value': [fouls.get('drawn') or 0, fouls.get('committed') or 0, cards.get('yellow') or 0, cards.get('red') or 0]
        })

        sns.set_theme(style="darkgrid", context="talk", rc={"axes.facecolor": "#12121a", "figure.facecolor": "#0d0d14", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white", "grid.color": "#2a2a35"})
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 9))
        fig.canvas.manager.set_window_title(f"{p['name']} - {league} {SEASON}")

        sns.barplot(x='Metric', y='Value', data=df_attack, ax=axes[0, 0], hue='Metric', palette="magma", legend=False)
        axes[0, 0].set_title('Attacking Output', color='#ffcc00', weight='bold')

        sns.barplot(x='Metric', y='Value', data=df_dribble, ax=axes[0, 1], hue='Metric', palette="crest", legend=False)
        axes[0, 1].set_title('Dribbling Performance', color='#00ffcc', weight='bold')

        sns.barplot(x='Metric', y='Value', data=df_pass, ax=axes[1, 0], hue='Metric', palette="viridis", legend=False)
        axes[1, 0].set_title(f"Pass Breakdown (Acc: {passes.get('accuracy') or 0}%)", color='#ff66cc', weight='bold')

        sns.barplot(x='Value', y='Metric', data=df_disc, ax=axes[1, 1], hue='Metric', palette="rocket", legend=False)
        axes[1, 1].set_title('Discipline & Physicality', color='#ff3333', weight='bold')

        fig.suptitle(f"{p['name']} Statistical Dashboard - {team} ({SEASON})", fontsize=20, fontweight='heavy', color='gold')

        patches_info = []
        for i, ax in enumerate(axes.flatten()):
            is_horiz = (i == 3)
            for patch in ax.patches:
                if is_horiz:
                    patches_info.append({'patch': patch, 'target': patch.get_width(), 'horiz': True})
                    patch.set_width(0)
                else:
                    patches_info.append({'patch': patch, 'target': patch.get_height(), 'horiz': False})
                    patch.set_height(0)

        def animate(frame):
            for info in patches_info:
                patch_obj = info['patch']
                if info['horiz']:
                    curr = patch_obj.get_width()
                    t = info['target']
                    patch_obj.set_width(curr + (t - curr) * 0.15)
                else:
                    curr = patch_obj.get_height()
                    t = info['target']
                    patch_obj.set_height(curr + (t - curr) * 0.15)
            return [info['patch'] for info in patches_info]

        ani = animation.FuncAnimation(fig, animate, frames=40, interval=20, blit=True, repeat=False)
        animations.append(ani)

        annots = []
        for i, ax in enumerate(axes.flatten()):
            annot = ax.annotate("", xy=(0,0), xytext=(0,20) if i!=3 else (20,0), textcoords="offset points",
                                bbox=dict(boxstyle="round4", fc="#2b2b36", ec="gold", lw=1.5, alpha=0.9),
                                arrowprops=dict(arrowstyle="-|>", color="gold"),
                                color="white", weight="bold", ha="center" if i!=3 else "left", va="bottom" if i!=3 else "center")
            annot.set_visible(False)
            annots.append((ax, annot, i==3))

        def on_hover(event):
            changed = False
            for ax, annot, is_horiz in annots:
                if event.inaxes == ax:
                    found = False
                    for patch_obj in ax.patches:
                        cont, _ = patch_obj.contains(event)
                        if cont:
                            if is_horiz:
                                val = patch_obj.get_width()
                                annot.xy = (val, patch_obj.get_y() + patch_obj.get_height()/2)
                            else:
                                val = patch_obj.get_height()
                                annot.xy = (patch_obj.get_x() + patch_obj.get_width()/2, val)
                            annot.set_text(f"{val:.0f}")
                            annot.set_visible(True)
                            found = True
                            changed = True
                            break
                    if not found and annot.get_visible():
                        annot.set_visible(False)
                        changed = True
                elif annot.get_visible():
                    annot.set_visible(False)
                    changed = True
            if changed:
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", on_hover)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

import pandas as pd
from esports_client import client

def get_draft_data(patch):
    """
    Queries and returns draft data for a given patch as a DataFrame.

    Parameters:
    - patch (str): The patch version for which the data is to be queried.

    Returns:
    - DataFrame: A pandas DataFrame containing the queried draft data.
    """
    PABcolumns = [
        'Team1Role1', 'Team1Role2', 'Team1Role3', 'Team1Role4', 'Team1Role5',
        'Team2Role1', 'Team2Role2', 'Team2Role3', 'Team2Role4', 'Team2Role5',
        'Team1Ban1', 'Team1Ban2', 'Team1Ban3', 'Team1Ban4', 'Team1Ban5',
        'Team1Pick1', 'Team1Pick2', 'Team1Pick3', 'Team1Pick4', 'Team1Pick5',
        'Team2Ban1', 'Team2Ban2', 'Team2Ban3', 'Team2Ban4', 'Team2Ban5',
        'Team2Pick1', 'Team2Pick2', 'Team2Pick3', 'Team2Pick4', 'Team2Pick5',
        'Team1', 'Team2', 'Winner', 'Team1Score', 'Team2Score',
        'Team1PicksByRoleOrder', 'Team2PicksByRoleOrder', 'OverviewPage'
    ]
    fields = ", ".join(
        [f"PAB.{column}" for column in PABcolumns] + ["SG.Patch", "SG.Winner", "SG.Team1Score", "SG.Team2Score"]
    )

    DraftData = client.cargo_client.query(
        tables="PicksAndBansS7=PAB, ScoreboardGames=SG",
        fields=fields,
        where=f"SG.Patch='{patch}'",
        join_on="PAB.GameId=SG.GameId",
        order_by="SG.DateTime_UTC DESC",
        limit="max"
    )

    # Convert the response to a DataFrame
    df = pd.DataFrame(DraftData)
    return df


def calculate_champion_stats(df, champion_filter=None):
    """
    Calculate champion statistics from the draft data DataFrame.

    Parameters:
    - df (DataFrame): The draft data as a pandas DataFrame.
    - champion_filter (str, optional): The champion name to filter statistics for.

    Returns:
    - DataFrame: A pandas DataFrame containing the calculated champion statistics.
    """
    champion_stats = {}

    def update_stats(champion, side, role, position, is_pick, is_winner):
        """
        Update the statistics for a specific champion.

        Parameters:
        - champion (str): The name of the champion.
        - side (str): The side (blue/red) the champion was picked on.
        - role (str): The role of the champion.
        - position (int): The pick position.
        - is_pick (bool): Whether the champion was picked.
        - is_winner (bool): Whether the champion's team won the game.
        """
        if champion not in champion_stats:
            champion_stats[champion] = {
                'champion': champion,
                'role': role,
                'games_played': 0,
                'win_count': 0,
                'blue_side_avg_pick_pos': 0,
                'red_side_avg_pick_pos': 0,
                'blue_side_pick_count': 0,
                'red_side_pick_count': 0,
                'blue_side_win_count': 0,
                'red_side_win_count': 0,
                'blue_side_winrate': 0,
                'red_side_winrate': 0,
                'winrate': 0
            }

        stats = champion_stats[champion]
        stats['games_played'] += 1
        if is_winner:
            stats['win_count'] += 1
            if side == 'blue':
                stats['blue_side_win_count'] += 1
            elif side == 'red':
                stats['red_side_win_count'] += 1

        if is_pick:
            stats['avg_pick_pos'] += position
            if side == 'blue':
                stats['blue_side_avg_pick_pos'] += position
                stats['blue_side_pick_count'] += 1
            else:
                stats['red_side_avg_pick_pos'] += position
                stats['red_side_pick_count'] += 1

    for index, row in df.iterrows():
        winner = row['Winner']
        team1_winner = winner == "1"
        team2_winner = winner == "2"

        for i in range(1, 6):
            team1_pick = row[f'Team1Pick{i}']
            team2_pick = row[f'Team2Pick{i}']
            team1_role = row[f'Team1Role{i}']
            team2_role = row[f'Team2Role{i}']

            update_stats(team1_pick, 'blue', team1_role, i, True, team1_winner)
            update_stats(team2_pick, 'red', team2_role, i, True, team2_winner)

    for stats in champion_stats.values():
        if stats['games_played'] > 0:
            stats['winrate'] = round((stats['win_count'] / stats['games_played']) * 100, 2)
            stats['avg_pick_pos'] = round(stats['avg_pick_pos'] / stats['games_played'], 1)
            if stats['blue_side_pick_count'] > 0:
                stats['blue_side_avg_pick_pos'] = round(stats['blue_side_avg_pick_pos'] / stats['blue_side_pick_count'], 1)
                stats['blue_side_winrate'] = round((stats['blue_side_win_count'] / stats['blue_side_pick_count']) * 100, 2)
            if stats['red_side_pick_count'] > 0:
                stats['red_side_avg_pick_pos'] = round(stats['red_side_avg_pick_pos'] / stats['red_side_pick_count'], 1)
                stats['red_side_winrate'] = round((stats['red_side_win_count'] / stats['red_side_pick_count']) * 100, 2)

    # Create a DataFrame with the filtered champion's stats if a champion_filter is provided
    if champion_filter:
        stats_df = pd.DataFrame([champion_stats.get(champion_filter, {})])
    else:
        stats_df = pd.DataFrame(champion_stats.values())

    return stats_df


def get_counterpicks(df, champion_name):
    """
    Get counterpicks against a specified champion.
    """
    counterpicks_details = []

    for index, row in df.iterrows():
        team1_picks = row['Team1PicksByRoleOrder'].split(',')
        team2_picks = row['Team2PicksByRoleOrder'].split(',')
        winner = row['Winner']
        team1_name = row['Team1']  # Assuming 'Team1' contains team name
        team2_name = row['Team2']  # Assuming 'Team2' contains team name

        if champion_name in team1_picks:
            position = team1_picks.index(champion_name)
            searched_champion_full_comp = team1_picks[:]
            opponent_full_comp = team2_picks[:]

            counterpicks_details.append({
                'Champion': f"{champion_name}",
                'Team': team2_name, # Team2 is the opponent
                'Tournament': row['OverviewPage'],  
                'Result': 'Win' if winner == "1" else 'Loss',
                f'{champion_name} Full Comp': searched_champion_full_comp,
                f'{team2_picks[position]} Full Comp': opponent_full_comp,
                'Winner': champion_name if winner == "1" else team2_picks[position]
            })
        elif champion_name in team2_picks:
            position = team2_picks.index(champion_name)
            searched_champion_full_comp = team2_picks[:]
            opponent_full_comp = team1_picks[:]

            counterpicks_details.append({
                'Champion': f"{champion_name} [{team2_name}-{row['OverviewPage']}]",
                'Result': 'Win' if winner == "2" else 'Loss',
                'Team': team1_name, # Team1 is the opponent
                'Tournament': row['OverviewPage'],  
                f'{champion_name} Full Comp': searched_champion_full_comp,
                f'{team1_picks[position]} Full Comp': opponent_full_comp,
                'Winner': champion_name if winner == "2" else team1_picks[position]
            })

    return counterpicks_details


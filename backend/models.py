from flask_restx import fields, Model

# Model for the champion stats response
champion_stats_model = Model('ChampionStats', {
    'champion': fields.String,
    'role': fields.String,
    'games_played': fields.Integer,
    'winrate': fields.Float,
    'blue_side_avg_pick_pos': fields.Float,
    'red_side_avg_pick_pos': fields.Float,
    'blue_side_pick_pct': fields.Float,
    'red_side_pick_pct': fields.Float
})

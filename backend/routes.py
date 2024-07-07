from flask import request, jsonify
from flask_restx import Namespace, Resource
from services import get_counterpicks, get_draft_data, calculate_champion_stats
from models import champion_stats_model
import pandas as pd
# Namespace for esports related operations
ns = Namespace('esports', description='LoL Esports operations')

@ns.route('/drafts/<string:patch>')
@ns.param('patch', 'The patch identifier')
class DraftList(Resource):
    '''Shows the draft information for a specific Patch'''

    @ns.doc('list_drafts')
    def get(self, patch):
        '''List draft information for a given patch'''
        try:
            result = get_draft_data(patch)
        except Exception as e:
            return {"error": str(e)}, 500

        return jsonify(result.to_dict(orient='records'))

@ns.route('/champion_stats')
class ChampionStats(Resource):
    '''Shows the statistics of champions'''

    @ns.doc('list_champion_stats')
    @ns.param('patch', 'The patch version to filter matches', required=True)
    @ns.param('champion', 'The champion name to filter statistics')
    def get(self):
        '''List statistics for champions for a given patch'''
        patch = request.args.get('patch')
        champion_filter = request.args.get('champion')

        try:
            draft_data = get_draft_data(patch)
        except Exception as e:
            return {"error": str(e)}, 500

        draft_df = pd.DataFrame(draft_data)
        if draft_df.empty:
            return {"error": "No draft data found for the given patch"}, 404

        stats_df = calculate_champion_stats(draft_df, champion_filter)
        if stats_df.empty:
            return {"error": "No statistics found for the given champion"}, 404

        return jsonify(stats_df.to_dict(orient='records'))
    
@ns.route('/counterpicks/<string:champion_name>')
@ns.param('champion_name', 'The name of the champion to find counterpicks against')
class Counterpicks(Resource):
    @ns.doc('list_counterpicks')
    @ns.param('patch', 'The patch version to filter matches', required=True)
    def get(self, champion_name):
        patch = request.args.get('patch')

        try:
            draft_data = get_draft_data(patch)
        except Exception as e:
            return {"error": str(e)}, 500

        if draft_data.empty:
            return {"error": "No draft data found for the given patch"}, 404

        counterpicks = get_counterpicks(draft_data, champion_name)
        if not counterpicks:
            return {"error": f"No counterpicks found for {champion_name}"}, 404

        return jsonify(counterpicks)
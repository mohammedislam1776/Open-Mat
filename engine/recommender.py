import json
from pathlib import Path

CATEGORIES = {'pin_escapes': 'Pin escapes', 'guard_passing': 'Guard passing', 'top_control': 'Top control', 'takedowns': 'Takedowns'}


def load_games():
    return json.loads((Path(__file__).resolve().parents[1] / 'data/games.json').read_text())


def rank_games(games, priorities, ruleset, recent_games=()):
    eligible = [g for g in games if g['category'] in priorities and ruleset in g['rulesets'] and g.get('review_status') in {'prototype_adaptation_pending_gym_review', 'gym_reviewed'}]
    return sorted(eligible, key=lambda g: (g['id'] in recent_games, priorities.index(g['category']), g['id']))

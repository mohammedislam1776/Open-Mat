import json
from pathlib import Path

CATEGORIES = {
    'pin_escapes': 'Pin escapes',
    'guard_passing': 'Guard passing',
    'top_control': 'Top control',
    'takedowns': 'Takedowns',
    'guard_offense': 'Guard offense',
    'guard_retention': 'Guard retention',
    'submission_offense': 'Submission offense',
    'submission_defense': 'Submission defense',
    'leg_entanglements': 'Leg entanglements',
}

REHEARSAL_CUES = {
    'pin_escapes': 'cooperative framing and guard recovery from the chosen pin',
    'guard_passing': 'lightly clearing the shield or knee line without forcing a trapped leg',
    'top_control': 'following slow hip turns with comfortable chest connection',
    'takedowns': 'familiar stance, entries, and balance recovery in a clear matted area',
    'guard_offense': 'cooperative hand-posting and shoulder connections without forced falls',
    'guard_retention': 'comfortable hip turns and rebuilding inside hand/foot connections without forced inversions',
    'submission_offense': 'unloaded grip/arm-separation entries; release at the target control, without finishing pressure',
    'submission_defense': 'gentle hand-fighting and early escapes with the controlling grip loose; release before joint or neck loading',
    'leg_entanglements': 'familiar unloaded leg connections and complete disengagement; no heel exposure, twisting, or finishes',
}


def load_games():
    return json.loads((Path(__file__).resolve().parents[1] / 'data/games.json').read_text())


def rank_games(games, priorities, ruleset, recent_games=()):
    eligible = [g for g in games if g['category'] in priorities and ruleset in g['rulesets'] and g.get('review_status') in {'prototype_adaptation_pending_gym_review', 'gym_reviewed'}]
    return sorted(eligible, key=lambda g: (g['id'] in recent_games, priorities.index(g['category']), g['id']))

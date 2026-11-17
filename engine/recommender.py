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

POSITION_LABELS = {
    'closed_guard': 'Closed guard',
    'half_guard': 'Half guard',
    'seated_open_guard': 'Seated open guard',
    'supine_open_guard': 'Supine open guard',
    'side_control': 'Side control',
    'hand_fighting': 'Hand fighting / knee touches',
    'single_leg': 'Single-leg situations',
    'clinch': 'Clinch / body lock',
    'armbar_control': 'Armbar control',
    'front_headlock': 'Front headlock',
    'open_guard_leg_connections': 'Open-guard leg connections',
    'straight_ashi': 'Straight ashi garami',
}

ELIGIBLE_STATUSES = {'prototype_adaptation_pending_gym_review', 'gym_reviewed'}


def available_positions(focus, games=None, ruleset=None):
    library = load_games() if games is None else games
    supported = {position for game in library if game['category'] == focus
                 and game.get('review_status') in ELIGIBLE_STATUSES
                 and (ruleset is None or ruleset in game['rulesets'])
                 for position in game.get('positions', [])}
    return [position for position in POSITION_LABELS if position in supported]


def focus_summary(priorities, position_preferences):
    return ' · '.join(CATEGORIES[p] + (f" — {POSITION_LABELS[position_preferences[p]]}" if position_preferences.get(p) else ' — Anything') for p in priorities)


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


def rank_games(games, priorities, ruleset, recent_games=(), position_preferences=None):
    positions = position_preferences or {}
    eligible = [g for g in games if g['category'] in priorities and ruleset in g['rulesets']
                and g.get('review_status') in ELIGIBLE_STATUSES
                and (not positions.get(g['category']) or positions[g['category']] in g.get('positions', []))]
    # A position-specific sequence stays ordered; Anything keeps the prior ranking.
    return sorted(eligible, key=lambda g: (
        priorities.index(g['category']),
        g.get('progression_order', 0) if positions.get(g['category']) else 0,
        g['id'] in recent_games,
        g['id'],
    ))

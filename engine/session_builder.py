from .recommender import CATEGORIES, load_games, rank_games
from .partner_adjustment import adjust_game
from .preparation import make_routine, load_exercises


def generate_session(user, games=None):
    priorities = user.get('priorities', [])
    if not isinstance(priorities, list) or not 1 <= len(priorities) <= 3 or len(set(priorities)) != len(priorities) or any(p not in CATEGORIES for p in priorities):
        raise ValueError('Choose one to three distinct supported priorities.')
    duration = user.get('duration', 60)
    structure = user.get('structure', 'balanced')
    partner = user.get('partner_skill', 'similar')
    ruleset = user.get('ruleset', 'no_gi')
    round_minutes = user.get('round_minutes', 5)
    if type(round_minutes) is not int or not 1 <= round_minutes <= 10:
        raise ValueError('Round length must be a whole number from 1 to 10 minutes.')
    if type(duration) is not int or duration not in (30, 60, 90):
        raise ValueError('Session length must be 30, 60, or 90 minutes.')
    if structure not in ('guided', 'balanced', 'exploratory') or partner not in ('lower', 'similar', 'higher') or ruleset not in ('gi', 'no_gi'):
        raise ValueError('Unsupported guidance, partner skill, or ruleset.')
    ranked = rank_games(load_games() if games is None else games, priorities, ruleset, user.get('recent_games', []))
    if any(not any(g['category'] == p for g in ranked) for p in priorities):
        raise ValueError('No compatible games for one or more priorities. Try another ruleset or library.')
    warm = user.get('warm_up_minutes', 20) if user.get('warm_up', True) else 0
    cool = user.get('wrap_up_minutes', 10) if user.get('cool_down', True) else 0
    if type(warm) is not int or warm not in (0,15,20,25) or type(cool) is not int or cool not in (0,5,10,15):
        raise ValueError('Choose a 15, 20, or 25-minute warm-up and a 5, 10, or 15-minute wrap-up, or disable a block.')
    equipment = user.get('preparation_equipment', 'none')
    excluded = user.get('excluded_preparation', [])
    if equipment not in ('none','bands') or not isinstance(excluded, list) or any(i not in {e['id'] for e in load_exercises()} for i in excluded):
        raise ValueError('Unsupported preparation equipment or excluded movement.')
    readiness = user.get('readiness', 'cold')
    if readiness not in ('cold','already_warm'):
        raise ValueError('Choose whether you are arriving cold or already warmed up.')
    standing = 'takedowns' in priorities or user.get('standing_preparation', False)
    available = duration - warm - cool
    minimum = max(5, round_minutes) * len(priorities)
    if available < minimum:
        raise ValueError(f'Warm-up ({warm} min) and wrap-up ({cool} min) leave {max(0,available)} min for games. Allow at least {minimum} min for your selected priorities: increase session length, edit preparation times, or choose fewer priorities. Preparation is never shortened automatically.')
    # Allocate whole rounds; keep leftover minutes visible as a transition/rest buffer.
    groups = [[g for g in ranked if g['category'] == p] for p in priorities]
    selected = [group[i] for i in range(max(map(len, groups))) for group in groups if i < len(group)][:min(6, available // max(5, round_minutes))]
    total_rounds, buffer_minutes = divmod(available, round_minutes)
    base, extra = divmod(total_rounds, len(selected))
    blocks = []
    def append(title, minutes, **details):
        start = sum(b['minutes'] for b in blocks)
        blocks.append(dict(title=title, minutes=minutes, start=start, end=start+minutes, **details))
    if warm:
        append('Progressive warm-up', warm, kind='warm_up', instructions='Raise temperature, move comfortably, activate lightly, then rehearse today’s tasks.', **make_routine('warm_up',warm,priorities,equipment,excluded,standing))
    for i, game in enumerate(selected):
        g = adjust_game(game, partner)
        round_count = base + (i < extra)
        buffer = buffer_minutes if i == len(selected)-1 else 0
        minutes = round_count * round_minutes + buffer
        start = sum(b['minutes'] for b in blocks)
        rounds = [dict(number=n+1, start=start+n*round_minutes, end=start+(n+1)*round_minutes, minutes=round_minutes) for n in range(round_count)]
        round_summary = f'{round_count} × {round_minutes}-minute round' + ('s' if round_count != 1 else '')
        if buffer:
            round_summary += f' + {buffer} min rest / transition buffer'
        append(g['name'], minutes, kind='game', game=g, rounds=rounds, round_minutes=round_minutes, round_count=round_count, buffer_minutes=buffer, round_summary=round_summary, hints=g['technique_hints'] if structure == 'guided' else g['technique_hints'][:1] if structure == 'balanced' else [], pacing='Agree on the start and resistance before the round. Reset after each success and continue until the round ends. Use the chosen role for the round; if trading roles, switch at the next round. No separate rest intervals are added between rounds; take needed rest within the allotted time or use the labeled buffer. Warm-up and wrap-up use their own phase timings.')
    if cool:
        append('Wrap up', cool, kind='cool_down', instructions='Gradually settle activity, move comfortably, and reflect.', **make_routine('cool_down',cool,priorities,equipment,excluded))
    return dict(schema_version=3, round_minutes=round_minutes, duration=duration, structure=structure, partner_skill=partner, ruleset=ruleset, priorities=priorities, blocks=blocks, prototype=True, preparation_equipment=equipment, readiness=readiness, excluded_preparation=excluded, standing_preparation=standing)


def plan_markdown(plan):
    lines = ['# OpenMat · Your session', f"{plan['duration']} minutes · {plan['structure'].title()} · {plan['ruleset'].replace('_', '-')} · Partner: {plan['partner_skill']} · {plan['round_minutes']}-minute rounds", '', 'Prototype game adaptations — pending gym review. Agree on resistance and resets. Stop on any tap, pain, or request.', '']
    for b in plan['blocks']:
        lines += [f"## {b['start']:02d}–{b['end']:02d} min · {b['title']}"]
        if b['kind'] != 'game':
            lines += [b['instructions'], b['notice'], b['caution'], '']
            for step in b['steps']:
                lines += [f"### {b['start']+step['start']:02d}–{b['start']+step['end']:02d} min · {step['title']}", step['instructions']]
                for exercise in step['exercises']:
                    lines += [f"- {exercise['name']}: {exercise['dose']} {exercise['cue']}", f"  Easier option: {exercise['easier_alternative']}"]
                    if exercise['source_url']:
                        lines += [f"  Movement reference: {exercise['source_url']}"]
            if b['aftercare']:
                lines += [b['aftercare']]
            lines += ['']
            continue
        g = b['game']
        lines += [f"Rounds: {b['round_summary']}"]
        for round in b['rounds']:
            lines += [f"- Round {round['number']}: {round['start']:02d}–{round['end']:02d} min ({round['minutes']} min)"]
        if b['buffer_minutes']:
            lines += [f"- {b['rounds'][-1]['end']:02d}–{b['end']:02d} min: rest / transition buffer; not a shortened round."]
        lines += [f"Start: {g['starting_position']} {g['adjusted_start']}", f"Your goal: {g['user_objective']}", f"Partner goal: {g['partner_objective']}", f"Reset: {g['reset_condition']}", b['pacing'], '', *['- '+x for x in g['rules']+g['safety_constraints']], *['- Practice cue: '+x for x in b['hints']], f"Source inspiration: {g['source_url']}", '']
    return '\n'.join(lines)

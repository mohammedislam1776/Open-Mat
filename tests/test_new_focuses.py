import itertools
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from engine import generate_session, plan_markdown
from engine.recommender import CATEGORIES, load_games, REHEARSAL_CUES

NEW_FOCUSES = ['guard_offense','guard_retention','submission_offense','submission_defense','leg_entanglements']


@pytest.mark.parametrize('focus,ruleset,structure,partner', list(itertools.product(NEW_FOCUSES,['gi','no_gi'],['guided','balanced','exploratory'],['lower','similar','higher'])))
def test_new_focus_end_to_end(focus,ruleset,structure,partner):
    plan=generate_session(dict(priorities=[focus],duration=60,ruleset=ruleset,structure=structure,partner_skill=partner,round_minutes=7))
    games=[b for b in plan['blocks'] if b['kind']=='game']
    assert len(games)==3
    assert {b['game']['category'] for b in games}=={focus}
    assert sum(b['minutes'] for b in plan['blocks'])==60
    assert REHEARSAL_CUES[focus] in plan['blocks'][0]['steps'][-1]['instructions']
    output=plan_markdown(plan)
    for b in games:
        game=b['game']
        original=next(g for g in load_games() if g['id']==game['id'])
        assert game['user_objective']==original['user_objective']
        assert game['partner_objective']==original['partner_objective']
        assert game['adjusted_start']==original['partner_variants'][partner]
        assert len(set(game['partner_variants'].values()))==3
        assert b['hints']==(game['technique_hints'] if structure=='guided' else game['technique_hints'][:1] if structure=='balanced' else [])
        assert all(r['minutes']==7 for r in b['rounds'])
        for text in [game['name'],game['user_objective'],game['reset_condition'],*game['rules'],*game['safety_constraints']]:
            assert text in output


@pytest.mark.parametrize('priorities', list(itertools.combinations(CATEGORIES,3)))
def test_every_three_focus_combination_keeps_selected_goals(priorities):
    plan=generate_session(dict(priorities=list(priorities),duration=60,round_minutes=10))
    games=[b for b in plan['blocks'] if b['kind']=='game']
    assert {b['game']['category'] for b in games}==set(priorities)
    assert all(b['round_count']>=1 for b in games)
    assert sum(b['minutes'] for b in plan['blocks'])==60


def test_catalog_and_control_only_policies():
    games=load_games()
    assert len({g['id'] for g in games})==len(games)
    for focus in NEW_FOCUSES:
        selected=[g for g in games if g['category']==focus]
        assert len(selected)==3
        for game in selected:
            assert game['review_status']=='prototype_adaptation_pending_gym_review'
            assert game['submission_policy']=='control_only'
            assert game['source_url'].startswith('https://slimemoldgrappling.com/games/')
            assert len(game['technique_hints'])==2
            if focus=='submission_defense':
                assert game['user_role']=='defender'
            if focus=='submission_offense':
                assert game['user_role']=='attacker'
            if focus=='leg_entanglements':
                rules=' '.join(game['rules']).lower()
                assert 'heel exposure' in rules and 'twisting' in rules
    assert next(g for g in games if g['id']=='GR03')['source_untested']
    assert next(g for g in games if g['id']=='GO03')['video_relationship'].startswith('source-linked')


@pytest.mark.parametrize('focus',NEW_FOCUSES)
def test_new_focus_ui_auto_refresh_and_exports(focus):
    app=AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py',default_timeout=15).run()
    next(b for b in app.button if b.label=='Build my session').click().run()
    app.multiselect[0].set_value([focus]).run()
    assert not app.exception
    plan=app.session_state['plan']
    assert plan['priorities']==[focus]
    assert {b['game']['category'] for b in plan['blocks'] if b['kind']=='game'}=={focus}
    assert CATEGORIES[focus] in ' '.join(c.value for c in app.caption)

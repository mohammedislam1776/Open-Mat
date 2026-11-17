import itertools
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest
from engine import generate_session, plan_markdown
from engine.recommender import CATEGORIES, POSITION_LABELS, available_positions, load_games, rank_games


@pytest.mark.parametrize('ruleset,structure,partner', list(itertools.product(['gi','no_gi'],['guided','balanced','exploratory'],['lower','similar','higher'])))
def test_closed_guard_is_a_real_filtered_progression(ruleset,structure,partner):
    plan=generate_session(dict(priorities=['guard_offense'],position_preferences={'guard_offense':'closed_guard'},duration=60,ruleset=ruleset,structure=structure,partner_skill=partner,round_minutes=7))
    blocks=[b for b in plan['blocks'] if b['kind']=='game']
    assert [b['game']['id'] for b in blocks]==['GO04','GO05','GO06']
    assert [b['game']['progression_order'] for b in blocks]==[1,2,3]
    assert all('closed_guard' in b['game']['positions'] for b in blocks)
    assert all(b['game']['adjusted_start']==b['game']['partner_variants'][partner] for b in blocks)
    assert sum(b['minutes'] for b in plan['blocks'])==60
    assert plan['position_preferences']=={'guard_offense':'closed_guard'}
    assert 'Closed guard' in plan['blocks'][0]['steps'][-1]['instructions']
    output=plan_markdown(plan)
    assert 'Guard offense — Closed guard' in output
    assert all(g['game']['name'] in output for g in blocks)
    assert 'Position: Closed guard' in output


@pytest.mark.parametrize('focus,position',[(f,p) for f in CATEGORIES for p in available_positions(f)])
def test_each_offered_position_has_matching_games(focus,position):
    for ruleset in ['gi','no_gi']:
        plan=generate_session(dict(priorities=[focus],position_preferences={focus:position},ruleset=ruleset))
        assert all(position in b['game']['positions'] for b in plan['blocks'] if b['kind']=='game')


def test_anything_preserves_unfiltered_selection():
    base=generate_session({'priorities':['guard_offense']})
    anything=generate_session({'priorities':['guard_offense'],'position_preferences':{'guard_offense':None}})
    assert base==anything
    assert set(g['positions'][0] for g in rank_games(load_games(),['guard_offense'],'gi'))=={'closed_guard','seated_open_guard','supine_open_guard'}


def test_position_filter_is_independent_for_each_focus():
    plan=generate_session(dict(priorities=['guard_offense','guard_retention','leg_entanglements'],position_preferences={'guard_offense':'closed_guard','guard_retention':'half_guard','leg_entanglements':'straight_ashi'}))
    for b in plan['blocks']:
        if b['kind']=='game':
            g=b['game']
            assert plan['position_preferences'][g['category']] in g['positions']


@pytest.mark.parametrize('positions',[[],{'unknown':'closed_guard'},{'guard_offense':'butterfly_guard'},{'guard_offense':[]},{'guard_offense':'side_control'}])
def test_invalid_position_choices_are_rejected(positions):
    with pytest.raises(ValueError):
        generate_session({'priorities':['guard_offense'],'position_preferences':positions})


def test_incompatible_position_never_falls_back_to_general_games():
    games=load_games()
    for g in games:
        if g['category']=='guard_offense' and 'closed_guard' in g['positions']:
            g['rulesets']=['gi']
    with pytest.raises(ValueError,match='will not substitute'):
        generate_session({'priorities':['guard_offense'],'position_preferences':{'guard_offense':'closed_guard'},'ruleset':'no_gi'},games)
    assert 'closed_guard' not in available_positions('guard_offense',games,'no_gi')


def test_metadata_is_consistent():
    for g in load_games():
        assert g['positions'] and set(g['positions'])<=POSITION_LABELS.keys()
        assert g['problems']
        assert isinstance(g['progression_order'],int)


def test_ui_position_selection_refreshes_and_clears_when_focus_removed():
    app=AppTest.from_file(Path(__file__).resolve().parents[1]/'app.py',default_timeout=15).run()
    app.multiselect[0].set_value(['guard_offense','guard_retention']).run()
    selector=next(s for s in app.selectbox if s.label=='Guard offense · Position / situation')
    selector.set_value('closed_guard').run()
    next(s for s in app.selectbox if s.label=='Guard retention · Position / situation').set_value('half_guard').run()
    next(b for b in app.button if b.label=='Build my session').click().run()
    assert not app.exception
    assert app.session_state['plan']['position_preferences']=={'guard_offense':'closed_guard','guard_retention':'half_guard'}
    next(s for s in app.selectbox if s.label=='Guard offense · Position / situation').set_value('supine_open_guard').run()
    assert not app.exception
    assert app.session_state['plan']['position_preferences']['guard_offense']=='supine_open_guard'
    app.multiselect[0].set_value(['guard_retention']).run()
    assert 'guard_offense' not in app.session_state['plan']['position_preferences']
    app.multiselect[0].set_value(['guard_retention','guard_offense']).run()
    assert next(s for s in app.selectbox if s.label=='Guard offense · Position / situation').value is None

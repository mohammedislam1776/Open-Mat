import itertools
import pytest
from engine import generate_session, plan_markdown
from engine.recommender import load_games, rank_games


def user(**updates):
    return dict(priorities=['pin_escapes'], duration=60, structure='balanced', partner_skill='similar', **updates)


@pytest.mark.parametrize('duration,structure,partner,warm,cool', list(itertools.product([30,60,90], ['guided','balanced','exploratory'], ['lower','similar','higher'], [True,False], [True,False])))
def test_session_contract(duration,structure,partner,warm,cool):
    inputs = dict(priorities=['pin_escapes','guard_passing','top_control'],duration=duration,structure=structure,partner_skill=partner,warm_up=warm,cool_down=cool)
    if duration - (20 if warm else 0) - (10 if cool else 0) < 15:
        with pytest.raises(ValueError, match='Preparation is never shortened'):
            generate_session(inputs)
        return
    plan = generate_session(inputs)
    assert sum(b['minutes'] for b in plan['blocks']) == duration
    assert plan['blocks'][0]['start'] == 0 and plan['blocks'][-1]['end'] == duration
    blocks = [b for b in plan['blocks'] if b['kind']=='game']
    assert {b['game']['category'] for b in blocks} == {'pin_escapes','guard_passing','top_control'}
    assert len({b['game']['id'] for b in blocks}) == len(blocks)
    assert all(b['minutes'] > 0 for b in blocks)
    assert all(bool(b['hints']) == (structure != 'exploratory') for b in blocks)


def test_partner_preserves_role_and_objective():
    for skill in ['lower','similar','higher']:
        plan = generate_session(dict(priorities=['pin_escapes'],partner_skill=skill))
        for b in plan['blocks']:
            if b['kind']=='game':
                g = b['game']
                original = next(x for x in load_games() if x['id']==g['id'])
                assert g['user_objective'] == original['user_objective']
                assert g['starting_position'] == original['starting_position']
                assert g['adjusted_start'] == original['partner_variants'][skill]


@pytest.mark.parametrize('patch', [dict(priorities=[]),dict(priorities=['unknown']),dict(priorities=['pin_escapes']*2),dict(duration=45),dict(partner_skill='mixed'),dict(structure='unknown'),dict(ruleset='unknown')])
def test_reject_invalid_inputs(patch):
    inputs=user(); inputs.update(patch)
    with pytest.raises(ValueError): generate_session(inputs)


def test_filter_and_no_compatible_library():
    games=load_games()
    games[0]['rulesets']=['gi']
    games[1]['review_status']='unfinished'
    with pytest.raises(ValueError): generate_session(user(),games)


def test_recent_games_rank_after_alternatives():
    ranked=rank_games(load_games(), ['pin_escapes'], 'gi', ['PE01'])
    assert ranked[0]['id']=='PE02'


def test_export_contains_entire_plan():
    plan=generate_session(user())
    output=plan_markdown(plan)
    assert all(b['title'] in output for b in plan['blocks'])
    assert 'Your goal:' in output and 'Reset:' in output


def test_default_preparation_and_export():
    plan=generate_session(user())
    warm,wrap=plan['blocks'][0],plan['blocks'][-1]
    assert (warm['minutes'],wrap['minutes'])==(20,10)
    assert [s['minutes'] for s in warm['steps']]==[5,5,4,6]
    assert [s['minutes'] for s in wrap['steps']]==[3,3,2,2]
    output=plan_markdown(plan)
    for block in (warm,wrap):
        assert sum(s['minutes'] for s in block['steps'])==block['minutes']
        for step in block['steps']:
            assert step['title'] in output
            for e in step['exercises']:
                assert e['dose'] in output and e['cue'] in output


@pytest.mark.parametrize('warm,wrap', list(itertools.product([15,20,25],[5,10,15])))
def test_editable_preparation_times(warm,wrap):
    plan=generate_session(dict(priorities=['pin_escapes'],duration=90,warm_up_minutes=warm,wrap_up_minutes=wrap))
    assert plan['blocks'][0]['minutes']==warm
    assert plan['blocks'][-1]['minutes']==wrap
    assert sum(b['minutes'] for b in plan['blocks'])==90


def test_band_substitutions_and_exclusions():
    no_kit=generate_session(user())
    exercises=[e for b in no_kit['blocks'] if b['kind']!='game' for s in b['steps'] for e in s['exercises']]
    assert all(not e['equipment'] for e in exercises)
    band=generate_session(dict(priorities=['pin_escapes'],preparation_equipment='bands',excluded_preparation=['band_steps','ground_rehearsal']))
    ids=[e['id'] for s in band['blocks'][0]['steps'] for e in s['exercises']]
    assert 'band_rotation' in ids
    assert not {'band_steps','ground_rehearsal','bridge','scapula'} & set(ids)
    assert 'excluded' in band['blocks'][0]['steps'][-1]['instructions']


@pytest.mark.parametrize('patch',[{'warm_up_minutes':5},{'wrap_up_minutes':8},{'preparation_equipment':'machine'},{'excluded_preparation':['unknown']}])
def test_invalid_preparation_options(patch):
    inputs=user(); inputs.update(patch)
    with pytest.raises(ValueError): generate_session(inputs)


def test_short_session_requires_explicit_time_adjustment():
    with pytest.raises(ValueError,match='leave 0 min'):
        generate_session(dict(priorities=['pin_escapes'],duration=30))
    plan=generate_session(dict(priorities=['pin_escapes'],duration=30,warm_up_minutes=15,wrap_up_minutes=5))
    assert sum(b['minutes'] for b in plan['blocks'] if b['kind']=='game')==10


@pytest.mark.parametrize('ruleset,structure,partner', list(itertools.product(['gi','no_gi'],['guided','balanced','exploratory'],['lower','similar','higher'])))
def test_takedown_focus(ruleset,structure,partner):
    plan=generate_session(dict(priorities=['takedowns'],duration=60,ruleset=ruleset,structure=structure,partner_skill=partner,standing_preparation=False))
    blocks=[b for b in plan['blocks'] if b['kind']=='game']
    assert len(blocks)==4
    assert all(b['game']['category']=='takedowns' for b in blocks)
    assert plan['standing_preparation'] is True
    assert 'stance movement' in plan['blocks'][0]['steps'][-1]['instructions']
    for b in blocks:
        assert b['game']['adjusted_start']==b['game']['partner_variants'][partner]
        assert b['game']['safety_constraints'] and b['game']['reset_condition']
    output=plan_markdown(plan)
    assert all(b['title'] in output for b in blocks)
    assert sum(b['minutes'] for b in plan['blocks'])==60


def test_mixed_takedown_focus_keeps_every_priority():
    plan=generate_session(dict(priorities=['takedowns','pin_escapes','guard_passing'],duration=60))
    assert {b['game']['category'] for b in plan['blocks'] if b['kind']=='game'}=={'takedowns','pin_escapes','guard_passing'}
    assert 'ground positions' in plan['blocks'][0]['steps'][-1]['instructions']


@pytest.mark.parametrize('round_minutes',range(1,11))
@pytest.mark.parametrize('duration',[60,90])
def test_rounds_have_selected_length_and_fit_session(round_minutes,duration):
    plan=generate_session(dict(priorities=['takedowns','pin_escapes','guard_passing'],duration=duration,round_minutes=round_minutes))
    assert plan['round_minutes']==round_minutes
    assert sum(b['minutes'] for b in plan['blocks'])==duration
    game_blocks=[b for b in plan['blocks'] if b['kind']=='game']
    assert {b['game']['category'] for b in game_blocks}=={'takedowns','pin_escapes','guard_passing'}
    for block in game_blocks:
        assert block['round_count']>=1
        assert len(block['rounds'])==block['round_count']
        assert block['rounds'][0]['start']==block['start']
        for r in block['rounds']:
            assert r['end']-r['start']==r['minutes']==round_minutes
        assert block['rounds'][-1]['end']+block['buffer_minutes']==block['end']
        assert sum(r['minutes'] for r in block['rounds'])+block['buffer_minutes']==block['minutes']
    assert sum(b['buffer_minutes'] for b in game_blocks)==(duration-30)%round_minutes


@pytest.mark.parametrize('invalid',[0,11,2.5,True,'5'])
def test_round_length_validation(invalid):
    with pytest.raises(ValueError,match='Round length'):
        generate_session(dict(priorities=['pin_escapes'],round_minutes=invalid))


def test_round_export_and_remainder_are_explicit():
    plan=generate_session(dict(priorities=['pin_escapes'],round_minutes=7))
    output=plan_markdown(plan)
    assert '7-minute rounds' in output
    assert '2 min rest / transition buffer' in output
    assert 'not a shortened round' in output
    for b in plan['blocks']:
        if b['kind']=='game':
            for r in b['rounds']:
                assert f"Round {r['number']}: {r['start']:02d}–{r['end']:02d} min (7 min)" in output


def test_long_rounds_need_one_full_round_per_priority():
    with pytest.raises(ValueError,match='at least 30 min'):
        generate_session(dict(priorities=['pin_escapes','guard_passing','takedowns'],duration=30,warm_up=False,cool_down=True,round_minutes=10))

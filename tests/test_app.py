from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_sidebar_changes_refresh_existing_plan():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py', default_timeout=15).run()
    assert not app.exception
    next(b for b in app.button if b.label == 'Build my session').click().run()
    assert not app.exception
    assert app.metric[0].value == '60 min'
    assert 'plan' in app.session_state
    app.select_slider[0].set_value(90).run()
    assert app.metric[0].value == '90 min'
    app.radio[0].set_value('exploratory').run()
    assert app.metric[2].value == 'Exploratory'
    app.selectbox[0].set_value('higher').run()
    assert app.session_state['plan']['partner_skill'] == 'higher'
    app.checkbox[3].uncheck().run()
    assert app.session_state['plan']['blocks'][-1]['kind'] == 'game'
    app.multiselect[0].set_value(['guard_passing']).run()
    assert app.session_state['plan']['priorities'] == ['guard_passing']


def test_partner_override_and_guidance():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py', default_timeout=15).run()
    app.checkbox[0].check().run()
    app.selectbox[1].set_value('higher')
    app.radio[0].set_value('guided')
    next(b for b in app.button if b.label == 'Build my session').click().run()
    assert not app.exception
    plan=app.session_state['plan']
    assert plan['partner_skill']=='higher'
    assert plan['structure']=='guided'
    assert all(len(b['hints'])==2 for b in plan['blocks'] if b['kind']=='game')


def test_empty_priorities_are_explained():
    app=AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py', default_timeout=15).run()
    next(b for b in app.button if b.label == 'Build my session').click().run()
    app.multiselect[0].set_value([]).run()
    assert not app.exception
    assert app.error and 'one to three' in app.error[0].value

    assert not app.metric
    assert 'plan' not in app.session_state
    app.multiselect[0].set_value(['top_control']).run()
    assert not app.error
    assert app.session_state['plan']['priorities'] == ['top_control']


def test_preparation_controls_update_plan_and_budget():
    app=AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py',default_timeout=15).run()
    next(b for b in app.button if b.label=='Build my session').click().run()
    assert app.session_state['plan']['blocks'][0]['minutes']==20
    assert app.session_state['plan']['blocks'][-1]['minutes']==10
    app.select_slider[0].set_value(30).run()
    assert app.error and not app.metric
    next(s for s in app.selectbox if s.label=='Warm-up minutes').set_value(15).run()
    next(s for s in app.selectbox if s.label=='Wrap-up minutes').set_value(5).run()
    assert not app.error
    assert app.metric[0].value=='30 min'
    next(r for r in app.radio if r.label=='Preparation equipment').set_value('bands').run()
    ids=[e['id'] for s in app.session_state['plan']['blocks'][0]['steps'] for e in s['exercises']]
    assert 'band_steps' in ids and 'bridge' not in ids


def test_legacy_session_plan_is_regenerated_before_rendering():
    from engine import generate_session
    legacy=generate_session({'priorities':['pin_escapes'],'duration':60})
    legacy.pop('schema_version')
    for block in legacy['blocks']:
        if block['kind']!='game':
            for key in ('notice','steps','caution','aftercare'):
                block.pop(key)
    app=AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py',default_timeout=15)
    app.session_state['plan']=legacy
    app.run()
    assert not app.exception
    assert app.session_state['plan']['schema_version']==3
    assert app.session_state['plan']['blocks'][0]['notice']
    assert app.metric[0].value=='60 min'


def test_takedowns_can_be_selected_and_enable_standing_preparation():
    app=AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py',default_timeout=15).run()
    app.multiselect[0].set_value(['takedowns']).run()
    next(b for b in app.button if b.label=='Build my session').click().run()
    assert not app.exception
    plan=app.session_state['plan']
    assert plan['standing_preparation']
    assert all(b['game']['category']=='takedowns' for b in plan['blocks'] if b['kind']=='game')
    assert next(c for c in app.checkbox if c.label=='Prepare for standing work too').disabled


def test_round_length_updates_automatically_and_is_visible():
    app=AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py',default_timeout=15).run()
    next(b for b in app.button if b.label=='Build my session').click().run()
    assert app.session_state['plan']['round_minutes']==5
    app.slider[0].set_value(7).run()
    assert not app.exception
    assert app.session_state['plan']['round_minutes']==7
    text=' '.join(m.value for m in app.markdown)
    assert 'Round length: 7 minutes' in text
    assert '7-minute round' in text
    for block in app.session_state['plan']['blocks']:
        if block['kind']=='game':
            assert all(r['minutes']==7 for r in block['rounds'])

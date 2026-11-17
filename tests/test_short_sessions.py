from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest
from engine import generate_session, plan_markdown


@pytest.mark.parametrize('duration',range(15,91,5))
@pytest.mark.parametrize('warm',[5,10,15,20,25])
def test_short_session_and_warm_up_budgets(duration,warm):
    settings=dict(priorities=['guard_offense'],position_preferences={'guard_offense':'closed_guard'},duration=duration,warm_up_minutes=warm)
    if duration-warm<5:
        with pytest.raises(ValueError,match='Preparation is never shortened'):
            generate_session(settings)
        return
    plan=generate_session(settings)
    assert sum(b['minutes'] for b in plan['blocks'])==duration
    assert sum(s['minutes'] for s in plan['blocks'][0]['steps'])==warm
    assert all(b['kind'] in ('warm_up','game') for b in plan['blocks'])
    assert 'Wrap up' not in plan_markdown(plan)


@pytest.mark.parametrize('duration',[5,10,16,19,91,100,True])
def test_invalid_session_length(duration):
    with pytest.raises(ValueError,match='5-minute increments'):
        generate_session(dict(priorities=['pin_escapes'],duration=duration))


def test_legacy_wrap_settings_do_not_restore_removed_wrap_up():
    plan=generate_session(dict(priorities=['pin_escapes'],cool_down=True,wrap_up_minutes=10))
    assert all(b['kind']!='cool_down' for b in plan['blocks'])
    assert sum(b['minutes'] for b in plan['blocks'])==60


def test_short_plan_ui_has_no_wrap_up_controls():
    app=AppTest.from_file(Path(__file__).resolve().parents[1]/'app.py',default_timeout=15).run()
    app.select_slider[0].set_value(15).run()
    next(s for s in app.selectbox if s.label=='Warm-up minutes').set_value(5).run()
    next(b for b in app.button if b.label=='Build my session').click().run()
    assert not app.exception
    assert app.metric[0].value=='15 min'
    assert not any('wrap' in s.label.lower() for s in app.selectbox)
    assert not any('wrap' in s.label.lower() for s in app.checkbox)


@pytest.mark.parametrize('warm',[0,1,4,6,26,True])
def test_enabled_warm_up_requires_five_minute_steps(warm):
    with pytest.raises(ValueError,match='5–25 minute warm-up'):
        generate_session({'priorities':['pin_escapes'],'warm_up_minutes':warm})

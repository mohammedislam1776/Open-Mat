import json
import streamlit as st
from engine import generate_session, plan_markdown
from engine.recommender import CATEGORIES, load_games
from engine.preparation import load_exercises

st.set_page_config(page_title='OpenMat · Train with intention', page_icon='🥋', layout='wide')
st.markdown('''<style>
.stApp {background:#f7f7f2;color:#172d29}
.block-container {max-width:1120px;padding-top:2.5rem}
h1,h2,h3 {color:#173f36}
.stButton>button[kind=primary] {background:#225c49;border:0;border-radius:8px}
[data-testid="stMetric"] {background:#e8eee5;padding:16px;border-radius:12px}
@media print {section[data-testid="stSidebar"],button,[data-testid="stDownloadButton"]{display:none!important}.stApp{background:white}}
</style>''', unsafe_allow_html=True)
st.caption('OPENMAT / SESSION PLANNER')
st.title('Step onto the mat with a plan.')
st.write('Choose your focus. Find the right challenge. Leave room to explore.')

with st.sidebar:
    st.header('Build your session')
    priorities = st.multiselect('What are you working on?', list(CATEGORIES), default=['pin_escapes'], format_func=CATEGORIES.get, max_selections=3)
    duration = st.select_slider('Time on the mat', [30, 60, 90], value=60, format_func=lambda n: f'{n} min')
    round_minutes = st.slider('Round length (minutes)', min_value=1, max_value=10, value=5, step=1)
    st.caption('Games use full rounds at this length. Any leftover time is labeled as rest / transition time.')
    structure = st.radio('How much guidance?', ['guided', 'balanced', 'exploratory'], index=1, format_func=str.title)
    st.caption('Guided adds technique cues. Balanced offers a hint. Exploratory keeps goals and rules. Choose independently of belt rank.')
    partner = st.selectbox('Partner’s skill in these positions', ['lower', 'similar', 'higher'], index=1, format_func={'lower':'Less experienced than me','similar':'Similar to me','higher':'More experienced than me'}.get)
    override = st.checkbox('Override the suggested starting advantage')
    start_choice = st.selectbox('Starting advantage (used only with override)', ['lower', 'similar', 'higher'], index=1, disabled=not override, format_func={'lower':'Give my partner an advantage','similar':'Use the standard start','higher':'Give me an advantage'}.get)
    effective_partner = start_choice if override else partner
    ruleset = st.radio('Training kit', ['no_gi', 'gi'], horizontal=True, format_func=lambda x: 'No-Gi' if x == 'no_gi' else 'Gi')
    st.subheader('Prepare & wrap up')
    st.caption('Proposed routines pending coach and physiotherapist review. Both count toward session time.')
    readiness = st.radio('Arriving on the mat', ['cold','already_warm'], format_func=lambda x: 'Cold / not yet prepared' if x == 'cold' else 'Already exercised')
    if readiness == 'already_warm':
        st.caption('Account for what you actually practiced and rehearse today’s positions. Sweat alone does not establish readiness. Edit timing yourself; the app will not shorten it automatically.')
    takedown_focus = 'takedowns' in priorities
    if takedown_focus:
        st.caption('Takedowns automatically include standing preparation. Starter games cover entries, connections, and controlled off-balancing; use a clear matted area and familiar coached movements.')
    standing = st.checkbox('Prepare for standing work too', disabled=takedown_focus) or takedown_focus
    if standing:
        st.caption('Adds familiar stance/entry rehearsal. Only use breakfalls already learned with a coach. The warm-up includes standing rehearsal alongside any selected ground priorities.')
    warm = st.checkbox('Include warm-up', value=True)
    warm_minutes = st.selectbox('Warm-up minutes', [15,20,25], index=1, disabled=not warm)
    cool = st.checkbox('Include wrap-up', value=True)
    cool_minutes = st.selectbox('Wrap-up minutes', [5,10,15], index=1, disabled=not cool)
    equipment = st.radio('Preparation equipment', ['none','bands'], format_func=lambda x: 'No equipment' if x == 'none' else 'Light long band + mini-loop available')
    if equipment == 'bands':
        st.caption('Inspect bands; use a secure anchor if required and keep equipment outside the rolling area. Band exercises replace selected activations; they are not extra sets.')
    exercises = load_exercises()
    excluded = st.multiselect('Exclude uncomfortable preparation movements', [e['id'] for e in exercises if e['stage'] not in ('reflection','check')], format_func=lambda i: next(e['name'] for e in exercises if e['id']==i))
    st.caption('Follow existing clinician restrictions. Exclusions do not generate rehabilitation advice. Skip any uncomfortable or unfamiliar grappling movement during rehearsal.')
    submitted = st.button('Build my session', type='primary', width='stretch')
    st.caption("After your first plan, changes update it automatically.")
    st.caption('Local prototype · No account required')

# Streamlit can retain session state from before a code update. Regenerate
# legacy plans using the current controls before rendering the new block shape.
saved_plan = st.session_state.get('plan')
if saved_plan and (saved_plan.get('schema_version') != 3 or any(
    not {'notice', 'steps', 'caution', 'aftercare'} <= block.keys()
    for block in saved_plan.get('blocks', []) if block.get('kind') != 'game'
)):
    st.session_state.pop('plan', None)
    st.session_state.planner_started = True

if submitted:
    st.session_state.planner_started = True

if st.session_state.get('planner_started', False):
    try:
        st.session_state.plan = generate_session(dict(priorities=priorities,duration=duration,structure=structure,partner_skill=effective_partner,ruleset=ruleset,warm_up=warm,cool_down=cool,warm_up_minutes=warm_minutes,wrap_up_minutes=cool_minutes,preparation_equipment=equipment,excluded_preparation=excluded,readiness=readiness,standing_preparation=standing,round_minutes=round_minutes))
    except ValueError as e:
        st.session_state.pop('plan', None)
        st.error(str(e))

plan = st.session_state.get('plan')
if plan:
    st.subheader('Your mat time, mapped out')
    a,b,c = st.columns(3)
    a.metric('Total time', f"{plan['duration']} min")
    b.metric('Focused games', sum(x['kind']=='game' for x in plan['blocks']))
    c.metric('Guidance', plan['structure'].title())
    st.markdown(f"**Round length: {plan['round_minutes']} minutes** · Applies to games; preparation keeps its phase timings.")
    st.caption('Focus: '+ ' · '.join(CATEGORIES[p] for p in plan['priorities']))
    st.info('Review this plan with your partner before starting. Screenshot the expanded cards or download a copy for the gym. Rest and resets are included in each block.')
    st.caption('Prototype adaptations, pending gym review. Partner adjustments and technique cues are OpenMat suggestions. No submissions in this starter library.')
    for block in plan['blocks']:
        with st.container(border=True):
            st.caption(f"{block['start']:02d}–{block['end']:02d} MIN / {block['minutes']} MINUTES")
            st.subheader(block['title'])
            if block['kind'] != 'game':
                st.write(block['instructions'])
                st.caption(block['notice'])
                for step in block['steps']:
                    st.markdown(f"**{block['start']+step['start']:02d}–{block['start']+step['end']:02d} min · {step['title']}**")
                    st.caption(step['instructions'])
                    for exercise in step['exercises']:
                        st.markdown(f"**{exercise['name']}** · {exercise['dose']}")
                        st.write(exercise['cue'])
                        st.caption('Easier option: '+exercise['easier_alternative'])
                    if step['exercises']:
                        with st.expander('Movement references & limits · '+step['title']):
                            for exercise in step['exercises']:
                                if exercise['source_url']:
                                    st.link_button(exercise['name']+' reference',exercise['source_url'])
                            st.caption(step['exercises'][0]['evidence_limits'])
                st.caption(block['caution'])
                if block['aftercare']:
                    st.write(block['aftercare'])
                continue
            st.markdown(f"**{block['round_summary']}**")
            st.caption(' · '.join(f"Round {r['number']}: {r['start']:02d}–{r['end']:02d} min" for r in block['rounds']))
            if block['buffer_minutes']:
                st.caption(f"{block['rounds'][-1]['end']:02d}–{block['end']:02d} min: rest / transition buffer. No shortened round.")
            g = block['game']
            st.markdown('**Start**')
            st.write(g['starting_position']+' '+g['adjusted_start'])
            left,right = st.columns(2)
            left.markdown('**Your objective**')
            left.write(g['user_objective'])
            right.markdown('**Partner’s objective**')
            right.write(g['partner_objective'])
            st.markdown('**Win / reset**')
            st.write(g['reset_condition'])
            st.markdown('**Constraints & safety**')
            for rule in g['rules']+g['safety_constraints']:
                st.write('• '+rule)
            for hint in block['hints']:
                st.write('Practice cue: '+hint)
            st.caption(block['pacing'])
            with st.expander('Source & partner variations'):
                st.link_button('Source inspiration',g['source_url'])
                st.link_button('Related video · not this exact game',g['video_url'])
                st.caption(g['source_note'])
                if g['source_untested']:
                    st.caption('The original source entry is also marked untested in the project notes.')
                for skill,variation in g['partner_variants'].items():
                    st.write(f'**{skill.title()} partner skill:** {variation}')
    a,b = st.columns(2)
    a.download_button('Download readable plan', plan_markdown(plan), 'openmat-session.md', 'text/markdown', width='stretch')
    b.download_button('Download session data', json.dumps(plan, indent=2), 'openmat-session.json', 'application/json', width='stretch')
else:
    st.subheader('Structure without losing the freedom to train.')
    a,b,c=st.columns(3)
    for col,title,body in [(a,'01 / Pick a focus','Work on pin escapes, guard passing, top control, or takedowns. Choose up to three priorities.'),(b,'02 / Set the challenge','Get starting conditions matched to your partner’s relative skill. Your objective stays the same.'),(c,'03 / Train uninterrupted','Generate the whole session before training. Every block includes goals, constraints, and resets.')]:
        with col.container(border=True):
            st.markdown('**'+title+'**')
            st.write(body)
    st.info('Use the sidebar to build your first session. Start with a familiar position and agree on comfortable resistance.')
with st.expander('About the starter library'):
    st.write('Ten prototype games cover four priorities, including standing entries and controlled off-balancing. They adapt summaries in your OpenMat Project Notes; timing, technique cues, and partner variants are app-authored. They have not been gym-tested. Unfinished source templates and ambiguous catalog entries are excluded.')
    for game in load_games():
        st.write(f"**{game['name']}** · {CATEGORIES[game['category']]} · Pending gym review")

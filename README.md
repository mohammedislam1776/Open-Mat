# OpenMat

A Streamlit prototype that builds a complete BJJ open-mat session before training. Based on OpenMat_Project_Notes.md and the prior feedback about uninterrupted practice, adjustable guidance, and partner-aware starts.

## Run

Requires Python 3.10 or later.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. Choose 1–3 priorities, 30/60/90 minutes, guidance, partner proficiency, and Gi/No-Gi, then build your plan. After the first build, sidebar changes refresh the plan automatically. Clearing all priorities removes the outdated plan and shows a validation message. Warm-up and wrap-up are enabled by default at 20 and 10 minutes, included in the time budget. Edit the warm-up to 15/20/25 minutes and wrap-up to 5/10/15 minutes, or disable either. A 30-minute session cannot fit the default preparation plus games: increase session length or explicitly adjust preparation. Each chosen priority needs at least five minutes of main work and one complete round; the planner never silently compresses preparation. Download Markdown for offline reference or JSON to retain structured session data. Browser printing is available through the browser menu; Markdown export is the reliable reference format.

## Implemented

- Ten prototype adaptations across pin escapes, guard passing, top control, and takedowns.
- Eligibility filtering, transparent ranking, priority interleaving, and exact time allocation.
- Partner variants that preserve the chosen role and objective; manual starting-advantage override.
- Guided technique cues, a Balanced hint, and Exploratory objectives and constraints.
- Complete plans with roles, starts, resets, pacing, safety constraints, source links, and exports.
- Pure Python engine independent of Streamlit and automated engine/UI tests.

```python
from engine import generate_session
plan = generate_session({
    'priorities': ['pin_escapes', 'guard_passing'],
    'duration': 60,
    'structure': 'balanced',
    'partner_skill': 'higher',
    'ruleset': 'no_gi',
    'warm_up': True,
    'cool_down': True,
    'warm_up_minutes': 20,
    'wrap_up_minutes': 10,
    'preparation_equipment': 'none',
    'excluded_preparation': [],
})
```

Run checks with `python -m pytest -q`.

## Content provenance and limits

`data/games.json` is a small, app-authored prototype library, adapted from summaries in the supplied project note. Source URLs are preserved; video references are related instruction, not demonstrations of the exact game. Partner adjustments, hints, timing, and some reset wording are OpenMat adaptations. None of these adaptations has been gym-reviewed. They are not presented as the full imported Slime Mold catalog or a validated curriculum. The knee-shield, side-control connection, and north-south transition source entries are marked untested in the note; all app entries remain pending review. Unfinished templates and entries with ambiguous outcomes were excluded.

No account, cloud storage, analytics, or external service calls are used by the planner. Plans live in Streamlit session memory and can be downloaded; restarting or losing the session can discard them. The interactive app requires its Python server; only downloaded/screenshot references work independently offline. Opening source/video links requires internet access.

Next: gym review of these six games, expand to a reviewed 10–15-game shortlist, then game swapping and a local training journal. Guard retention, submissions, timers, persistent history, and learned recommendations are not implemented.

## Preparation and wrap-up templates

The updated project note supplies the proposed 20-minute warm-up (5 general movement + 5 mobility + 4 activation + 6 task rehearsal) and 10-minute wrap-up (3 easy movement + 3 comfortable mobility + 2 body check + 2 optional reflection). These are detailed in the cards and Markdown/JSON exports, including doses, easier options, movement-reference links, evidence limits, and pending-review status.

`data/preparation.json` stores exercise metadata; `engine/preparation.py` composes timed phases. The band preset assumes both a light long band and mini-loop are available. It replaces bridges and scapular push-ups with lateral steps and external rotations; it does not add extra work or claim equivalent loading. No-equipment plans use no equipment-dependent exercises. Exclusions remove movements without inventing rehabilitation alternatives; when a phase is empty, its time remains available for rest or the user's existing approved preparation.

Arrival readiness is contextual and does not automatically reduce warm-up time. Optional standing preparation uses familiar stance/entry work and previously coached breakfalls; selecting Takedowns enables standing preparation automatically, including in mixed-focus sessions. The journal is a reflection prompt only, not persistent logging. Separate progressive strength conditioning from the note is outside this change.

All preparation templates remain proposed and pending physiotherapist/coach review. Movement-reference links are inherited from the supplied note and are not claims that the linked guides validate the whole sequence. No injury-prevention or soreness-prevention benefit is promised. Existing clinician restrictions take precedence.

## Takedown focus

The Takedowns priority includes four proposed games from the note's standing catalog: knee touches, single-leg connection and movement, body-lock hand connection, and controlled single-leg off-balancing to hands or hips. The first three prohibit completed takedowns and lifts. The fourth allows only a slow controlled descent, uses familiar coached movements, and directs partners to the connection-only task if they cannot receive the movement safely. No airborne finishes, slams, or sacrifice throws are included. All four support Gi/No-Gi, every guidance level, and partner-relative starting adjustments while preserving the task. Knee Tag retains its source's untested flag. All adaptations remain pending gym review.

## Round length

Choose a whole-minute round length from 1 through 10 minutes in the sidebar (default: 5). Changing it updates an existing plan automatically. The session header and every game show the chosen duration, number of rounds, and each round's session-clock start/end. Games are allocated whole rounds; any leftover minutes are labeled as a rest/transition buffer at the end of the last game, never silently shortened rounds. Warm-up/wrap-up keep their own phase timings. No additional between-round rest time is added outside the session budget.

Set `round_minutes` in `generate_session` inputs to use the same behavior without the UI. The Markdown and JSON downloads include round details. If the time budget cannot fit one whole round per priority, the planner asks for a timing/priority adjustment.

## Community Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for exact Community Cloud settings. Use `app.py` on `main`, Python 3.11, and no secrets. The GitHub test workflow verifies the app before updates are deployed.

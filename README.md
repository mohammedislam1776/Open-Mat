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

Open the local URL printed by Streamlit. Choose 1–3 focuses and optional positions, then select 15–90 minutes in five-minute increments. Warm-up is optional; when enabled choose 5–25 minutes in five-minute increments (20-minute default). All warm-up time counts toward the session. Wrap-up is no longer part of the planner. Each chosen priority needs at least five minutes of main work and one complete round; incompatible budgets show an explicit message instead of silently shortening preparation. After the first build, setting changes update the plan automatically. Download Markdown or JSON for reference.

## Implemented

- 28 prototype adaptations across nine focuses: pin escapes, guard passing, top control, takedowns, guard offense, guard retention, submission offense, submission defense, and leg entanglements.
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
    'warm_up_minutes': 20,
    'preparation_equipment': 'none',
    'excluded_preparation': [],
})
```

Run checks with `python -m pytest -q`.

## Content provenance and limits

`data/games.json` is a small, app-authored prototype library, adapted from summaries in the supplied project note. Source URLs are preserved; video references are related instruction, not demonstrations of the exact game. Partner adjustments, hints, timing, and some reset wording are OpenMat adaptations. None of these adaptations has been gym-reviewed. They are not presented as the full imported Slime Mold catalog or a validated curriculum. The knee-shield, side-control connection, and north-south transition source entries are marked untested in the note; all app entries remain pending review. Unfinished templates and entries with ambiguous outcomes were excluded.

No account, cloud storage, analytics, or external service calls are used by the planner. Plans live in Streamlit session memory and can be downloaded; restarting or losing the session can discard them. The interactive app requires its Python server; only downloaded/screenshot references work independently offline. Opening source/video links requires internet access.

Next: gym review of the prototype games, game swapping, and a local training journal. Submission finishing rounds, timers, persistent history, and learned recommendations are not implemented.

## Warm-up templates

Choose 5, 10, 15, 20, or 25 minutes, or disable warm-up. A 15-minute session with a 5-minute warm-up leaves 10 minutes for games. The short five-minute routine uses two minutes of general movement, one minute of comfortable mobility, and two minutes of task rehearsal. It omits a separate activation circuit. The ten-minute routine uses 3/2/2/3 minutes for general movement, mobility, light activation, and rehearsal. Longer routines retain their more detailed phase timings. These are proposed templates, not validated BJJ injury-prevention protocols.

`data/preparation.json` contains warm-up movements only. `engine/preparation.py` composes the phase timings and adjusts the movement count/dose for shorter routines. The band preset replaces selected activations when that phase is included; the five-minute routine has no band circuit. Exclusions do not invent rehabilitation alternatives. Readiness does not automatically reduce preparation time. Takedowns enable standing rehearsal. No wrap-up or journal block is generated, even if older callers send legacy `cool_down`/`wrap_up_minutes` fields.

## Takedown focus

The Takedowns priority includes four proposed games from the note's standing catalog: knee touches, single-leg connection and movement, body-lock hand connection, and controlled single-leg off-balancing to hands or hips. The first three prohibit completed takedowns and lifts. The fourth allows only a slow controlled descent, uses familiar coached movements, and directs partners to the connection-only task if they cannot receive the movement safely. No airborne finishes, slams, or sacrifice throws are included. All four support Gi/No-Gi, every guidance level, and partner-relative starting adjustments while preserving the task. Knee Tag retains its source's untested flag. All adaptations remain pending gym review.

## Round length

Choose a whole-minute round length from 1 through 10 minutes in the sidebar (default: 5). Changing it updates an existing plan automatically. The session header and every game show the chosen duration, number of rounds, and each round's session-clock start/end. Games are allocated whole rounds; any leftover minutes are labeled as a rest/transition buffer at the end of the last game, never silently shortened rounds. Warm-up keeps its own phase timings. No additional between-round rest time is added outside the session budget.

Set `round_minutes` in `generate_session` inputs to use the same behavior without the UI. The Markdown and JSON downloads include round details. If the time budget cannot fit one whole round per priority, the planner asks for a timing/priority adjustment.

## Community Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for exact Community Cloud settings. Use `app.py` on `main`, Python 3.11, and no secrets. The GitHub test workflow verifies the app before updates are deployed.

## Guard, submission, and leg-entanglement focuses

The expanded focuses use app-authored adaptations of the supplied catalog summaries; Guard offense now includes three additional closed-guard games:

| Focus | Starter tasks |
| --- | --- |
| Guard offense | Create hand posts; connect behind shoulders; open-guard off-balancing |
| Guard retention | Stay upright seated; rebuild inside connections; retain the knee shield |
| Submission offense | Complete figure-four grip; separate an armbar defense; create triangle-entry alignment |
| Submission defense | Free the arm from unloaded armbar control; deny figure-four connection; escape unloaded front-headlock control |
| Leg entanglements | Maintain leg/hip connection; build an entanglement; capture the ankle without finishing |

Submission offense is explicitly an entry/control focus in this version. Defense preserves the user's defender role for every partner level. These games do not permit submission finishes or finishing pressure. Leg-entanglement tasks prohibit heel exposure and twisting, and call for complete release if a foot/knee is trapped or pressure appears. They do not introduce heel-hook or 50/50 finishing rounds. All records preserve source/video relationships and untested flags, while app variants, hints, and reset adaptations are labeled as such. No new game is claimed to be gym-validated.

Each focus works independently or in any combination of up to three priorities. Warm-up rehearsal now includes task-specific cues. Guidance, partner starts, Gi/No-Gi, round scheduling, and Markdown/JSON exports apply to every new focus. The live app is https://openmat-planner.streamlit.app/.

## Position / situation selection

Each selected focus has its own **Position / situation** menu directly below the focus selector. **Anything** uses the whole focus library. A specific position is a strict eligibility filter, independently applied to that focus; other focuses retain their own choices. Unsupported or incompatible choices produce an error rather than substituting another position. Only positions with playable records appear in the UI.

All games now carry `positions`, `problems`, and `progression_order` metadata. The data model supports multiple position tags per game, but tags describe supported starts rather than merely the destination of a transition. Problem metadata prepares for more specific future filtering; there is no separate problem selector in this release.

**Guard offense → Closed guard** selects a three-game sequence: break posture and establish upper-body connections; create meaningful hand posts; develop a hip-to-shoulder attacking angle. These remain positional games with objectives and constraints, not mandatory technique repetitions. Their order is preserved for a position-specific selection even if recent-game history is provided. Other guard-offense starts are Seated open guard and Supine open guard. Future positions such as butterfly or 50/50 need curated game records before appearing as choices.

The pure-engine input is a mapping keyed by selected focus:

```python
plan = generate_session({
    'priorities': ['guard_offense', 'guard_retention'],
    'position_preferences': {
        'guard_offense': 'closed_guard',
        'guard_retention': 'half_guard',
    },
    'duration': 60,
})
```

Omit a focus key or use `None` for Anything. The plan and Markdown/JSON downloads preserve these choices; warm-up rehearsal uses the selected positions. Partner adjustments change the challenge while retaining position and user objective. App-authored rules, source provenance, no-finishing restrictions, and pending-review labels remain in place.

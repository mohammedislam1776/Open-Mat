---
title: OpenMat — Product Concept and Development Plan
aliases:
  - OpenMat
  - BJJ Open Mat Planner
tags:
  - projects/openmat
  - software-development
  - bjj
  - recommendation-systems
status: planning
updated: 2026-10-21
---

# OpenMat — Product Concept and Development Plan

> [!abstract] Project summary
> **OpenMat** is a personalized Brazilian Jiu-Jitsu (BJJ) open-mat session planner. It generates a complete training session *before* open mat based on technical priorities, available time, preferred level of guidance, and the relative skill of training partners. Its core philosophy is **structure without sacrificing autonomy**: users get objectives, starting positions, and constraints while retaining freedom to experiment and troubleshoot.

## 1. Problem and product vision

**Original idea:** Give people useful drills and games when they have spare open-mat time, do not know what to practice, or do not want another full roll, without requiring paid instructionals or apps. The pre-generated session planner develops that idea into a complete plan while preserving the option to practice a short block and then find a roll.

**Problem:** During open mats, practitioners may default to unstructured rolling without deliberately working on weaknesses. Constantly consulting a phone to decide the next activity would itself waste training time.

**Solution:** Generate a ready-to-follow, 30–90-minute plan *before* stepping onto the mats. The user can review, save, print, or screenshot it. Post-session reflection is optional.

**Core design principles**
- **Plan once, train uninterrupted:** Avoid requiring phone interaction between rounds.
- **Objectives over prescriptions:** Positional games should generally specify starting conditions, goals, and constraints rather than force particular moves.
- **Adjustable guidance:** Less experienced users, or experienced users in unfamiliar positions, can request specific technique suggestions.
- **Partner-aware challenge:** Adjust starting advantages and rules for the relative skill of a training partner.
- **User autonomy:** The user can override recommendations and eventually swap individual games.
- **Training-goal preservation:** Changing partner difficulty should not accidentally replace the skill the user wants to practice.
- **Open-mat etiquette:** Support productive downtime while leaving room for training with others; avoid making the app a reason to disengage from partners.

## 2. Decisions made so far

| Topic | Working decision | Rationale |
|---|---|---|
| Product format | Complete pre-generated session | Minimizes phone checks during training |
| Primary content | Positional games with objectives and constraints | Allows experimentation and personal technique choices |
| Structure | User-selectable guidance levels | Beginners may need more instruction; experience alone should not dictate mode |
| Partner skill | Relative-skill adjustments | Creates appropriate challenges for different partners |
| First recommendation engine | Transparent, rule-based logic | Easier to implement, inspect, and test before sufficient training data exists |
| Initial platform | Python + Streamlit web app | Fast path to a working MVP |
| Long-term learning | Optional feedback-driven personalization | Possible once useful, reliable outcome data exist |

## 3. User feedback and feature implications

### Original idea
- Generate drills and positional games based on the user's strengths, weaknesses, and priorities.
- Example: a user frequently pinned in side control practices escaping that position.
- Example: a user struggling to maintain or finish from top plays a game where top maintains/submits and bottom escapes.
- Initially envisioned as a decision-tree-based system.

### Feedback: avoid mid-session phone use
- **Insight:** A plan that constantly asks what to do next could consume precious rolling time.
- **Implication:** Generate the entire session beforehand; allow offline reference via screenshot or printout.

### Feedback: adjustable structure
- **Insight:** Experienced practitioners may prefer broad positional constraints, while beginners may want explicit techniques and repetitions.
- **Implication:** Separate *exercise selection* from *how instructions are presented*.
- **Important nuance:** Belt rank/experience and desired structure are separate attributes. An advanced practitioner learning an unfamiliar area may still prefer detailed guidance.

### Friend's feedback: account for partner skill
- **Suggested default:**
  - **Less experienced partner:** Give the partner a positional advantage.
  - **Similar experience:** Start in a neutral position.
  - **More experienced partner:** Give the user a positional advantage.
- **Implication:** Introduce partner-difficulty calibration while keeping the target skill constant.
- **Nuance:** Belt rank is only a rough proxy for position-specific skill. Relative proficiency can vary by domain, e.g., guard passing versus takedowns.
- **Open design question:** Should adjustments aim for competitive balance, or deliberately create difficult constraints for skill development? Potentially support both later.

## 4. Training structure modes

| Mode | Intended experience | Example: bottom side control |
|---|---|---|
| **Guided** (high structure) | Named techniques, steps, repetition or round suggestions | Establish frames, practice elbow-knee escape, then increase resistance |
| **Balanced** (moderate structure) | Starting position, objectives, constraints, optional hints | Bottom escapes/recovers guard; top maintains pin; any suitable escape allowed |
| **Exploratory** (low structure) | Minimal instructions, open experimentation | Start pinned; bottom escapes; top controls; experiment with strategies |

**Architecture principle:** One underlying game should support multiple instructional presentations, rather than creating separate copies of the same game for each mode.

## 5. Partner-adjusted games

**Example objective: guard passing**

| Relative partner skill | Possible starting configuration | User objective |
|---|---|---|
| Less experienced | Partner begins with established grips/frames | Pass despite initial disadvantage |
| Similar experience | Neutral open-guard engagement | Establish and complete a pass |
| More experienced | User begins with favorable grips or partial passing position | Complete and consolidate the pass |

**Example objective: side-control escapes**
- Partner skill should affect starting frames, top-player restrictions, allowed transitions, or resistance—not automatically change the user from escaping to attacking.
- Partner adjustments should be *suggested defaults*, with manual overrides.
- Mixed/rotating partners could use a printed set of three variants for the same game.

## 6. MVP scope

### Must-have for version 0.1
- [ ] Select 1–3 technical priorities.
- [ ] Choose session length (30, 60, or 90 minutes).
- [ ] Choose Guided, Balanced, or Exploratory mode.
- [ ] Specify relative partner skill (less, similar, more experienced).
- [ ] Store a curated library of ~20–30 positional games, starting with five complete records and a gym-tested shortlist of 10–15 favorites.
- [ ] Curate that shortlist from the [[#16. Game library|112-entry research catalog]]; exclude unfinished/test entries and review source ambiguities before import.
- [ ] Tag games by position, goal (retention, sweep, pass, submission), Gi/No-Gi, intensity, and equipment/partner requirements. Track solo drills separately from the partner-only Slime Mold games.
- [ ] Filter and rank compatible games.
- [ ] Generate a full session with allocated durations, roles, starting positions, rules, win/reset conditions, and safety constraints.
- [ ] Include a specific warm-up and wrap-up sequence, with 20-minute/10-minute editable defaults and no-equipment/band options; count both within session time. See [[#Warm-up, wrap-up, and injury-risk reduction]].
- [ ] Display a readable, screenshot-friendly training plan.
- [ ] Add basic automated tests.

### Valuable after the core MVP
- [ ] Replace one recommended game without rebuilding the whole session.
- [ ] Support rotating partners and mixed partner levels.
- [ ] Collect optional post-session outcomes and perceived difficulty through a frictionless journal: game/drill, duration, RPE, and an optional note, with an automatic timestamp.
- [ ] Save previous plans and training priorities.
- [ ] Export/print plans.
- [ ] Track multiweek progression.

### Defer until validated
- [ ] Accounts and profiles across devices.
- [ ] Building or hosting a large instructional-video catalog. External YouTube references are already collected in the game library; reviewing and presenting them in the app remains separate work.
- [ ] Social/community features.
- [ ] React frontend / mobile-native app.
- [ ] Machine-learned recommendations or contextual bandits.

### Earlier feature ideas and follow-up scope

The original picker-first MVP also included a live timer and two-tap journal. The working version 0.1 scope above centers on generating a full session before training; the following ideas remain available for later prioritization.

- **Quick drill/game picker:** Filter for 5, 10, or 20 minutes, solo versus partner, position, goal, Gi/No-Gi, equipment, and intensity. A constrained randomizer can provide variety without requiring learned recommendations.
- **Timer:** Support timed rounds or repetition-based drills, with a simple transition from “practice for X minutes” to finding a roll. Keep it optional so the plan does not require phone checks between rounds.
- **Local-first journal:** Aim for two-tap logging, automatic timestamps, optional notes, and export. Extend the optional post-session feedback flow rather than building a separate logging system.
- **Video and points tracking:** Record rolls locally by default, respect gym recording policies, and manually tag clips to games. Track takedowns, passes, back takes, and similar events. Consider AI footage analysis only after the core product is useful.
- **Health and heart rate:** If an iOS version is built, start with Apple Health trends over time. Avoid live “do/don’t roll” alerts; consider third-party integrations such as Sensay only if users want them.
- **Injury adjustments:** Use allowlists/blocklists for movements or games, such as excluding bridging or favoring static retention. Keep suggestions conservative and avoid medical, rehabilitation, or physical-therapy advice.

### Offline use, privacy, and validation

- **Offline goal:** The original concept requires the library, timer, and journal to work with poor gym WiFi, with cloud sync optional. Screenshot/print access supports offline reference in the Streamlit MVP; full offline interactive use remains an implementation requirement to resolve, not an existing capability.
- **Privacy and safety:** Default recorded footage to local storage, honor gym recording policies, and include appropriate limits around injury, movement, and heart-rate information.
- **Test early:** Try a simple list of 10–15 favorite games plus a timer at the gym, then refine the curated library and generated plans from actual use.

## Warm-up, wrap-up, and injury-risk reduction

**Product intent:** Treat preparation and finishing as planned parts of the session, with specific exercises and equipment alternatives. **Default proposal: 20 minutes to warm up and 10 minutes to wrap up**, both included in the chosen session length. Five minutes can be the initial general-movement phase; it should not be OpenMat's entire default warm-up.

### What the evidence supports

A survey of 1,140 BJJ athletes found the knee and shoulder were the most frequently injured sites; many injuries occurred during sparring, submissions, and takedowns. This supports prioritizing joint control alongside safe partner behavior. It does not show that any particular warm-up prevents those injuries. [BJJ injury study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8721390/)

Exercise-based warm-up programs combining movement, strength, balance, and coordination have reduced some injury outcomes in other sports. For example, a football trial found fewer overall, severe, and overuse injuries, although its primary lower-limb injury result was not statistically significant. **Applying that approach to BJJ is an extrapolation.** The routines below are proposed OpenMat templates, not a tested BJJ prevention protocol or a guarantee against ligament, meniscus, tendon, neck, or submission injuries. [Warm-up trial](https://pubmed.ncbi.nlm.nih.gov/19066253/)

Keep three functions distinct:

- **Before training:** Raise temperature, explore comfortable movement, lightly activate muscles, and progressively rehearse grappling tasks.
- **Across the week:** Build strength and control through progressive conditioning. A light band circuit immediately before rolling does not replace this.
- **After training:** Gradually settle activity, move comfortably, and reflect. Do not promise that stretching or cooling down prevents injury or next-day soreness.

> [!important] Appropriate use
> These templates assume an adult who can exercise comfortably and has no current injury requiring restrictions. Use comfortable ranges and stop movements that cause sharp pain, joint instability, numbness, or dizziness. A recent injury, surgery, recurrent dislocation, or ongoing symptoms needs an individualized clinician/physiotherapist plan. The exercise guides below include rehabilitation material; they illustrate movements, not a diagnosis or return-to-sport clearance.

### Default warm-up: 20 minutes

Aim to finish **warm, coordinated, and ready to increase effort**, without exhausting the grip, shoulders, or legs. Use controlled repetitions and comfortable ranges, rather than forcing flexibility.

| Time | Phase | No-equipment template | Equipment alternative |
| --- | --- | --- | --- |
| 0–5 min | Raise temperature | Build from brisk marching or easy jogging into gentle lateral shuffles and stance movement. Keep a conversational pace. | Easy bike or rowing machine if available; increase gradually. |
| 5–10 min | Dynamic mobility | About one minute each: ankle rocks with heels down; shallow squats/hip hinges; gentle adductor rock-backs from hands/knees with one leg out to the side; thoracic rotations on all fours; wrist motion, hand opening/closing, and comfortable arm circles. Use roughly 5–8 controlled repetitions per side where applicable. | No equipment is necessary. A wall can support balance. Avoid using a band to force extra range. |
| 10–14 min | Light activation | One easy set each: 8 glute bridges, 6–8 scapular push-ups from hands/knees, 4 bird dogs per side, and 20 seconds of single-leg balance per side. Rest/transition in the remaining time. | Swap bridges for 6–8 small lateral band steps each way, and scapular push-ups for 8 light band external rotations per side. Keep bird dogs and balance. |
| 14–20 min | Grappling-specific ramp | 2 min of easy shrimping, bridges through the shoulders rather than the head, and technical stand-ups; 2 min cooperative movement through the day's positions; 2 min of a simple positional task with gradually increasing resistance and no submission finishes. | Same sequence; put bands away before partner work. For a takedown session, use stance/entries and previously learned, coached breakfalls instead of ground transitions. |

The mobility and activation selections adapt general joint-conditioning exercises and BJJ movement practice; **the exact sequence, doses, and 20-minute duration are design choices**. AAOS recommends an initial 5–10 minutes of low-impact activity before its conditioning exercises, which is one reason to distinguish general warming from the complete preparation sequence. [AAOS shoulder guide](https://www.orthoinfo.org/recovery/rotator-cuff-and-shoulder-conditioning-program/)

**Adjusting the duration**

- **Arriving cold or stiff, or preparing for harder standing work:** Allow 20–25 minutes; use extra time for gradual movement and task rehearsal, not harder stretching.
- **Short technical session:** A 15-minute option can use 4 min general movement + 4 min mobility + 3 min activation + 4 min task rehearsal. Reduce subsequent training intensity/volume rather than rushing into hard rounds.
- **Already warmed up:** Account for what was actually done and rehearse the new session's positions. Feeling sweaty alone does not establish readiness for every task.
- **After a long idle period:** Repeat some general movement and task rehearsal before resuming harder work.
- **Short on time:** Shorten the main training block. Do not automatically compress preparation to five minutes to fit more rolling.

These are flexible planning ranges, not medical minimums. If movements remain uncomfortable or poorly controlled, change the session rather than treating completion of the timer as clearance.

### Exercise menu for common areas of concern

Choose a few relevant movements; **do not perform the entire table before every session**. Equipment options are alternatives, not identical exercises or equal loads. The aim is general strength/control around commonly stressed areas; none makes a joint safe to force through a submission.

| Area / BJJ concern | Without exercise equipment | With bands or simple equipment | Light preparation dose and cues |
| --- | --- | --- | --- |
| **Knees:** knee control during passing, scrambling, and standing | Shallow squat; supported split squat; single-leg balance. Keep the foot stable and knee tracking with the toes. | Mini-band lateral steps with band above knees; low step-ups using a stable step. | Choose one strength movement for 6–8 easy reps per side, or balance for 20 sec/side. Avoid twisting on a planted foot. These do not specifically prove prevention of ACL/MCL or meniscus injuries. [Knee guide](https://www.orthoinfo.org/recovery/knee-conditioning-program/) |
| **Hips, groin, and hamstrings:** control in wide or flexed positions | Glute/heel-dig bridge; side-lying hip abduction or adduction; gentle adductor rock-back. For adduction, bend the top leg and place its foot in front, then lift the straight lower leg slightly. | Mini-band bridge or lateral steps; gentle pillow/soft-ball squeeze between knees. | Choose one activation for 6–10 reps, or 3 gentle squeezes of 5 sec. Keep pelvis steady and avoid forcing wide splits. [Hip guide](https://www.orthoinfo.org/recovery/hip-conditioning-program/) |
| **Shoulders:** cuff/scapular control during frames and pulling | Scapular push-up from hands/knees: keep elbows straight and move the shoulder blades; wall slide within comfortable range. | Light band row; external rotation with elbow bent and held at the side, rotating the forearm outward without turning the trunk. | 1 easy set of 8–10. Keep shoulders relaxed; avoid end-range forcing or a large pre-roll fatigue circuit. [Shoulder guide](https://www.orthoinfo.org/recovery/rotator-cuff-and-shoulder-conditioning-program/) |
| **Elbows and forearms:** pulling load and grip-related irritation | Gentle elbow bends/straightening; forearm palm-up/palm-down rotation; wrist-extension isometric resisted by the opposite hand. | Light band curls/triceps extensions; supported wrist extension using a light band or small bottle. | 6–10 controlled reps, or 3 gentle 5-sec isometrics. Keep the forearm supported for wrist work; no heavy grip burnout before rolling. Strength does not protect an elbow from a finished armbar. [Elbow/wrist guide](https://www.cuh.nhs.uk/patient-information/elbow-and-wrist-strengthening-exercises/) |
| **Hands and fingers:** repetitive gi gripping and awkward finger loading | Open/close hands gently; tendon-glide sequence through straight fingers, hook fist, and comfortable fist. Do not force the joints. | Light therapy putty squeeze or gentle finger opening against a loose finger-extension loop. | 5 slow glide cycles or 8 light repetitions. Movement/conditioning options, not proof against finger sprains or tendon injuries. Avoid aggressively stretching a painful or swollen finger. [Hand movement guide](https://www.nth.nhs.uk/resources/hand-therapy-tendon-gliding-exercises/) |
| **Ankles and feet:** balance and control during standing/transitions | Calf raises, ankle rocks, and single-leg balance near support. | Light band dorsiflexion/plantarflexion: draw toes toward shin, then point away against resistance. | 8–10 easy reps or 20 sec balance per side. Use support if needed; do not force a trapped foot or treat strength as protection from ankle locks. [Ankle guide](https://www.orthoinfo.org/recovery/foot-and-ankle-conditioning-program/) |
| **Trunk/back and rib area:** control under movement and pressure | Bird dog; short side plank from knees; controlled hip bridge. | Light band anti-rotation press: stand side-on to a secure anchor, hold band at chest, press forward without twisting. | 4–6 slow bird dogs/side or a 10–15 sec side plank. Choose one. These train trunk control; they are not proven protection from rib compression injuries. [Spine guide](https://www.orthoinfo.org/recovery/spine-conditioning-program/) |
| **Neck:** comfortable motion and low-load control | Gentle turns and small chin nods. If comfortable and familiar, keep head still while gently resisting a hand at the forehead or temple. | No neck-band/harness loading in the default library. A clinician/qualified coach can individualize progression; equipment is optional. | 3–5 easy movements per direction, or 2–3 gentle 5-sec holds each chosen direction. No neck bridges, headstands, forceful partner stretches, or loaded end-range neck work in the default routine. [Neck exercise guidance](https://msk-bexley.nhs.uk/conditions/neck-pain/mechanical-neck-pain) |

**Small optional kit:** A light long resistance band, a light mini-loop, and an optional soft ball/therapy putty cover most swaps. Inspect bands and use a secure anchor outside the rolling area; never leave loose bands on the mat. A band row, for example, trains pulling more directly than a scapular push-up, so the app should describe the different purpose rather than call every swap equivalent.

### Conditioning between BJJ sessions

For longer-term capacity, add **two manageable strength sessions per week**, adjusted around existing training. General public-health guidance supports training major muscle groups on at least two days weekly with bodyweight or resistance equipment. This frequency is not a proven BJJ injury-prevention dose. [NHS strength guidance](https://www.nhs.uk/live-well/exercise/how-to-improve-strength-flexibility/)

A simple starting template is **one squat/split-squat, one hip/hamstring movement, one push, one pull when equipment is available, one calf/balance exercise, and one trunk exercise**. Rotate small cuff/forearm work into the week. Begin with one easy set while learning, then build toward 2 sets of 8–12 controlled reps; isometrics and balance use time instead. On separate conditioning days, progress resistance gradually while leaving a few good repetitions in reserve. Do not turn the pre-roll activation block into this strength session or automatically add it after an exhausting open mat.

For a no-kit session, use split squats, heel-dig bridges, push-ups at a suitable level, calf raises, and side planks/bird dogs. With bands, add rows, external rotations, and lateral steps. Neck work remains low-load and individualized. These templates are suggestions for review, not treatment for a current injury.

### Default wrap-up: 10 minutes

**Goal:** Leave training gradually, move comfortably, and capture what to change next time. Keep this restorative rather than adding a final conditioning challenge.

| Time | Activity | Specific options |
| --- | --- | --- |
| 0–3 min | Lower activity gradually | Walk slowly around the mat; let breathing settle. No final burpee or grip-strength finisher. |
| 3–6 min | Comfortable mobility | Choose 2–3: gentle calf stretch, half-kneeling hip-flexor stretch with a small pelvic tuck, easy cross-body shoulder stretch, or unloaded wrist/finger motion. For stretches, hold about 20–30 sec/side without bouncing or forcing. Skip irritated areas. |
| 6–8 min | Relaxed breathing and body check | Sit or lie comfortably and breathe normally, letting the exhale lengthen if comfortable. No breath holds or hyperventilation. Notice new pain, swelling, or reduced function; do not try to stretch those symptoms away. |
| 8–10 min | Optional journal and next-session adjustment | Log games, duration, RPE, one useful observation, and any symptom that should change the next plan. A body check is not an injury diagnosis. |

Bands are not necessary for wrapping up. If desired, use a supported shoulder movement or a few very light rows **instead of** one mobility choice; do not add another strength circuit. Foam rolling is optional for comfort, not a required injury-prevention step, and should not press directly on a painful joint or the neck.

Do not describe the wrap-up as “flushing lactic acid” or preventing soreness. A randomized trial of unfamiliar eccentric exercise found no apparent soreness benefit from its cool-down intervention; it was not a BJJ trial. The app should offer wrap-up for a gradual transition, comfort, and reflection without promising recovery effects. [Cool-down trial](https://pubmed.ncbi.nlm.nih.gov/17535144/)

Afterward, rehydrate, eat according to normal recovery needs, change out of damp training clothes, and follow gym hygiene practices. New or persistent symptoms should change subsequent training and prompt appropriate assessment, rather than trigger an automated “safe to roll” message.

### How OpenMat should implement this

- [ ] Include warm-up and wrap-up in total session time, enabled by default with editable durations. Show the specific sequence, not just a generic timer.
- [ ] Offer **no-equipment** and **band available** presets, with exercise-by-exercise substitutions and illustrated source links.
- [ ] Ask whether the user is arriving cold or has already exercised, and whether the session includes standing work.
- [ ] Let users exclude uncomfortable movements and apply existing clinician restrictions. Do not automatically prescribe rehabilitation from a pain score.
- [ ] Keep mobility, light activation, and progressive strength work as different content types with different doses.
- [ ] Store equipment, body region, stage, reps/hold time, intensity, easier alternative, restrictions, source URL, evidence limits, and review status for each exercise.
- [ ] Have a sports physiotherapist and experienced BJJ coach review the templates before presenting them as app defaults.
- [ ] Validate that the session builder counts preparation and wrap-up time and never substitutes unavailable equipment.

## 7. Exercise data model

Start with a JSON library; move to SQLite when sessions, user preferences, and feedback require persistence.

```json
{
  "id": "SC001",
  "name": "Side Control Escape Game",
  "category": "pin_escapes",
  "skills": ["framing", "guard_recovery"],
  "starting_position": "bottom_side_control",
  "user_objective": "escape_or_recover_guard",
  "partner_objective": "maintain_control",
  "duration_minutes": 5,
  "difficulty": 2,
  "structure_options": ["guided", "balanced", "exploratory"]
}
```

**Fields to consider adding:** success condition, reset condition, ruleset, safety constraints, allowed/forbidden transitions, equipment/partner requirements, intensity, technique hints, and partner-adjustment variants. Preserve source URLs, YouTube references, source-linked versus related-video labels, review status, and any untested/template flags when importing the research catalog.

**Initial app coverage:** Pin escapes, guard passing, and top control. Expand the playable subset later to guard retention, takedowns, submissions, and other positions. The broader [[#16. Game library|research catalog]] already includes these areas, scrambles, and striking; inclusion in the note does not make a game validated or in scope for the first release.

## 8. Recommendation architecture

```text
User inputs
  ├─ priorities and weaknesses
  ├─ duration
  ├─ desired structure
  ├─ partner relative skill
  └─ constraints
        ↓
Game eligibility filter
        ↓
Rule-based relevance ranking
        ↓
Partner-position / difficulty calibration
        ↓
Session builder and time allocation
        ↓
Guidance-level formatting
        ↓
Complete pre-open-mat plan
        ↓
Optional post-session feedback
```

**Avoid one enormous decision tree.** Use small modules with distinct responsibilities. A hand-coded decision tree is a **rule-based expert system**, not a machine-learned decision tree.

### Simple heuristic scoring

$$
S_i = w_1G_i + w_2D_i + w_3V_i
$$

Where $G_i$ is goal alignment, $D_i$ is difficulty suitability, and $V_i$ is variety. Initial weights are developer-defined and should be tested rather than presented as learned parameters.

```python
def score_game(game, user):
    score = 0
    if game["category"] in user["priorities"]:
        score += 5
    if game["difficulty"] == user["difficulty"]:
        score += 3
    if game["id"] not in user["recent_games"]:
        score += 2
    return score
```

### Optional optimization extension

Choose compatible exercises to maximize relevance under a time budget:

$$
\max \sum_i x_i s_i \quad \text{subject to} \quad \sum_i x_i t_i \leq T
$$

Here $x_i$ is a binary selection variable, $s_i$ the relevance score, $t_i$ duration, and $T$ available time. More constraints could enforce variety, partner requirements, and fatigue limits. This is a **later enhancement**, not necessary for version 0.1.

## 9. Example generated 60-minute session

**User priority:** Side-control escapes and guard retention. **Mode:** Balanced.

| Time | Activity | Rules/objective |
|---|---|---|
| 20 min | Progressive warm-up | 5 min general movement + 5 min dynamic mobility + 4 min light activation + 6 min grappling-specific ramp; see [[#Warm-up, wrap-up, and injury-risk reduction]] |
| 12 min | Side-control escape games | Bottom escapes/recovers guard; top maintains; alternate roles |
| 12 min | Guard-retention games | Bottom retains/recovers guard; top passes; alternate roles |
| 6 min | Constraint-based sparring | Start in target positions, then transition to freer rolling at an agreed intensity |
| 10 min | Wrap-up | 3 min easy movement + 3 min comfortable mobility + 2 min relaxed breathing/body check + 2 min optional reflection |

**Total: 60 minutes, including preparation and wrap-up.** This is an illustrative product template, not a validated training prescription. Increase total available time or reduce main-work volume when more preparation is needed.

## 10. Technical stack and repository layout

**Recommended MVP:** Python, Streamlit, JSON, pytest, Git/GitHub. Add SQLite when persistence is needed. Consider FastAPI, PostgreSQL, Docker, and React only after the basic application is useful.

```text
openmat/
├── app.py
├── data/
│   └── games.json
├── engine/
│   ├── recommender.py
│   ├── partner_adjustment.py
│   └── session_builder.py
├── models/
│   └── schemas.py
├── tests/
│   └── test_recommender.py
├── requirements.txt
└── README.md
```

**Key engineering principle:** `generate_session(user)` must run and be testable without launching Streamlit.

```python
user = {
    "priorities": ["pin_escapes"],
    "duration": 60,
    "structure": "balanced",
    "partner_skill": "higher",
    "difficulty": 2,
    "recent_games": []
}

plan = generate_session(user)
print(plan)
```

The function above is a **target interface to implement**, not completed code.

## 11. Six-week implementation roadmap

> [!note] Planning assumption
> Rough estimate: 8–12 hours per week, potentially longer while learning web development.

- [ ] **Week 1 — Define and curate:** Requirements, skill taxonomy, 20–30 games in JSON (start with five).
- [ ] **Week 2 — Recommendation engine:** Eligibility filtering, scoring, selection.
- [ ] **Week 3 — Partner and session logic:** Relative-skill adjustments, guidance modes, round and time allocation.
- [ ] **Week 4 — Streamlit UI:** Inputs, readable generated plans, optional game swapping.
- [ ] **Week 5 — User testing:** Ask 3–5 BJJ practitioners to try it and collect feedback.
- [ ] **Week 6 — Testing and deployment:** Automated tests, README, GitHub repository, public prototype.

### Suggested automated tests
- [ ] Prioritizing guard retention produces relevant games.
- [ ] Partner adjustment does not erase the target skill.
- [ ] Total session time, including warm-up and wrap-up, does not exceed the chosen duration.
- [ ] Guided mode includes technique-level instructions.
- [ ] Repetition is avoided when alternatives exist.
- [ ] Incompatible or unsafe configurations are rejected or flagged.
- [ ] Mixed partner settings yield understandable prewritten variations.

Have experienced practitioners review the library for practical appropriateness and safety.

## 12. Potential ML and data science extensions

Only pursue these once sufficient *real, reliable* feedback exists.

- **Feedback collection:** Starting position, partner relative proficiency, rule adjustments, outcome, perceived difficulty, perceived usefulness.
- **Progress tracking:** Success rates and skill trends over repeated sessions, with attention to changing partner quality and context.
- **Difficulty calibration:** Predict whether a configuration is too easy, appropriately challenging, or too hard.
- **Adaptive recommendations:** Compare learned models against the transparent rule-based baseline.
- **Contextual bandits:** Eventually explore the tradeoff between proven exercises and potentially useful alternatives.
- **Evaluation:** Track user-rated usefulness, completed sessions, recommendation acceptance, and learning-related outcomes. Do not assume higher immediate win rates always imply better learning.

**Research opportunity:** Test whether desired structure and effective structure vary by experience and familiarity with the position; don't assume belt rank alone determines the answer.

## 13. Resume and LinkedIn positioning

**Working project title:** OpenMat — Personalized BJJ Training Recommendation System.

**Resume bullets (use only after the features are actually implemented):**
- Developed a rule-based recommendation engine that generates personalized BJJ training sessions from technical priorities, experience, and time constraints.
- Designed partner-aware positional games that adjust starting advantages and constraints while preserving technical objectives.
- Built and deployed an interactive Python application for generating structured open-mat plans, with automated tests for recommendation logic and session scheduling.

**Potential later bullet, only if implemented:**
- Implemented constrained optimization to allocate training time across relevant positional games.

**Portfolio story:** Complements quantitative/text-analysis research with product development, recommendation-system design, structured data, testing, and deployment. Avoid calling the hand-written rule system “machine learning.”

## 14. Open questions

- [ ] Should the user choose *balanced challenge* versus *deliberate disadvantage*?
- [ ] How should partner proficiency be assessed: self-report, belt, position-specific skill, or a combination?
- [ ] How many priorities should one session address without diluting focus?
- [ ] How should game duration and work/rest intervals be determined?
- [ ] How should games reset after a successful escape, pass, or submission?
- [ ] Should structure level be session-wide or adjustable for each game?
- [ ] What is the simplest useful post-session feedback prompt?
- [ ] Which ruleset, safety restrictions, and accessibility assumptions belong in the exercise schema?
- [ ] What qualifies as a good recommendation in user testing?

## 15. Immediate next actions

1. Create the `openmat` repository and Python environment.
2. Write down the input and output contract for `generate_session(user)`.
3. Create **five** complete positional-game records in `games.json`.
4. Write the simplest filter-and-rank implementation.
5. Generate one sensible 30- or 60-minute plan in the terminal before building a UI.

## 16. Game library

Source: [Slime Mold Grappling](https://slimemoldgrappling.com/games/index.html).

Checked **2026-10-21** against the site's Games menu and [sitemap](https://slimemoldgrappling.com/sitemap.xml): **112 catalog entries — 107 games with written tasks, four unfinished templates, and one test placeholder**. Every catalog entry has its own source and a YouTube reference below. Same-named games remain separate when their positions or rules differ.

These are compact, paraphrased picker descriptions. Follow the linked source for the complete starting grips, constraints, and reset conditions. A continuous task has no terminal win unless the source specifies one. All games require a partner.

**Video key:** **S** = a video linked by Slime Mold on the game or its corresponding lesson plan; **R** = related instruction about the position or skill, not a claim that the video demonstrates the exact site game. Videos are reused across related variations. Titles, creators, and current availability were checked; full transcripts were unavailable. A video may show finishes or movements that a particular game prohibits.

**Source status:** † means the source marks the entry *untested*. Keep unfinished templates and the test placeholder out of the playable app picker until rules are supplied.

> [!warning] Training constraints
> Agree on the task and reset before starting. Honor each game's no-submission, no-takedown, no-hook, or no-grip restrictions. For finishing familiarization, increase pressure slowly, tap early, and release immediately. Leg-control games prohibit finishes where stated; release if an escape becomes unsafe. Striking games use controlled, light tags.

### Guard — Seated Guard (7)

| Game / source                                                                                                                           | Setup, task, and win or reset                                                                                                                                                                                                         | YouTube reference                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [Structure and Connections](https://slimemoldgrappling.com/games/guard_games/seated_guard/structure_and_connections/index.html)         | Start seated with feet inside a kneeling partner’s knees. Bottom maintains an upright, connected guard; top strips connections and wins by flattening bottom onto their back.                                                         | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |
| [Causing Posts](https://slimemoldgrappling.com/games/guard_games/seated_guard/causing_posts/index.html)                                 | Use the same seated-versus-kneeling start. Bottom off-balances top to provoke repeated hand posts; top clears grips and tries to flatten bottom. Bottom has no separate terminal win.                                                 | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |
| [Connect to the Shoulders](https://slimemoldgrappling.com/games/guard_games/seated_guard/connect_to_the_shoulders/index.html)           | From seated guard against a kneeling partner, bottom first forces a post, then wins by securing double underhooks and joining their hands. Top wins by flattening bottom.                                                             | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |
| [Create and Break Connections](https://slimemoldgrappling.com/games/guard_games/seated_guard/create_and_break_connections/index.html) † | Seated bottom begins with one shin/ankle and one hand attached to standing top’s legs. Bottom builds and retains connections; top strips them. No sweeps; continuous connection work.                                                 | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |
| [Control A Leg](https://slimemoldgrappling.com/games/guard_games/seated_guard/control_the_leg/index.html) †                             | Use the connected seated-versus-standing start. Top clears the knee line and stays at the thighs, without passing farther. Bottom off-balances top toward hands or hips and sustains hand posts. No explicit terminal win.            | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |
| [Destabilization](https://slimemoldgrappling.com/games/guard_games/seated_guard/destabilization/index.html) †                           | From connected seated guard, top wins by achieving a chest-to-chest or chest-to-back pin. Bottom uses leg connections to off-balance and improve position. The source’s bottom objective and stated win differ; check the full rules. | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |
| [Punishing Posts](https://slimemoldgrappling.com/games/guard_games/seated_guard/punishing_posts/index.html)                             | Seated bottom faces kneeling top with feet inside. Bottom forces hand posts and keeps those hands grounded; top strips connections and tries to flatten bottom. Bottom’s task is continuous.                                          | **R** [Guard games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=X_DMrrud25I) |

### Guard — Supine / Closed Guard (5)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Create and Break Connections](https://slimemoldgrappling.com/games/guard_games/supine_guard/closed_guard/create_and_break_connections/index.html) — posture | Closed guard with top kneeling: top clears grips and regains posture; bottom keeps posture broken. Top may neither stand nor open/pass guard; bottom may neither sweep nor submit. Continuous. | **R** [Breaking posture in closed guard — Jon Thomas](https://www.youtube.com/watch?v=ZKsfnBbBdjk) |
| [Open the Feet](https://slimemoldgrappling.com/games/guard_games/supine_guard/closed_guard/opening_the_feet/index.html) | From kneeling inside closed guard, top works toward separating bottom’s crossed feet. Bottom uses grips and posture control to keep the guard closed, without sweeps or submissions. Reset when the feet open. | **R** [Breaking closed guard — Marcelo Garcia](https://www.youtube.com/watch?v=032wIsVv0hY) |
| [Stand Up](https://slimemoldgrappling.com/games/guard_games/supine_guard/closed_guard/stand_up/index.html) | Begin with top kneeling inside closed guard. Top wins by standing; bottom tries to prevent that through grip and posture control. Bottom does not sweep or submit. Reset after top stands. | **R** [Breaking closed guard — Marcelo Garcia](https://www.youtube.com/watch?v=032wIsVv0hY) |
| [Create and Break Connections](https://slimemoldgrappling.com/games/guard_games/supine_guard/closed_guard/hip_and_shoulder_connection/index.html) — hip-to-shoulder connection † | Hip-to-shoulder variant: start in kneeling closed guard. Bottom wins by bringing their hips to a shoulder outside top’s arms. Top strips upper-body control, without standing or opening/passing guard. | **R** [Closed guard arm drag to back — Hurricane Jiu Jitsu](https://www.youtube.com/watch?v=eolJrphVaCU) |
| [Climbing the Back](https://slimemoldgrappling.com/games/guard_games/supine_guard/closed_guard/to_the_back/index.html) † | Start with bottom’s hips already beside top’s shoulder, legs wrapped around the torso. Bottom seeks chest-to-back contact for three seconds; top disengages or inserts knees/feet. Top must not stand while bottom remains attached. | **R** [Closed guard arm drag to back — Hurricane Jiu Jitsu](https://www.youtube.com/watch?v=eolJrphVaCU) |

### Guard — Supine / Shin Surfing (1)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Shin Surfing](https://slimemoldgrappling.com/games/guard_games/supine_guard/shin_surfing/index.html) | Begin with top’s shin pinning one thigh, using chosen upper-body grips. Top maintains shin contact between hip and knee without advancing or submitting. Bottom wins by recovering feet inside, standing, or reversing. | **R** [Knee Ride — Craig Jones](https://www.youtube.com/watch?v=zmdJMYmLNt0) |

### Guard — Supine / Half Guard (7)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Underhook Control](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/underhook_control/index.html) | Start in half guard with top chest-to-chest and double underhooks. Top holds the pin and frees the trapped leg to pass; bottom wins by removing the underhooks. Reset after either success. | **R** [Double-under passing — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=-BJrPT7VfEI) |
| [Single Underhook Control](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/single_underhook_control/index.html) | Start chest-to-chest in half guard with top holding one underhook and bottom framing the head-side arm. Top seeks double underhooks; bottom seeks a knee shield or inside hook. Reset after either success. | **R** [Double-under passing — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=-BJrPT7VfEI) |
| [Hip Access](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/hip_access/index.html) | Bottom starts on their side with top already accessing the hips. Top flattens, underhooks, and frees the trapped leg; bottom recovers a knee shield or inside hook. | **R** [Double-under passing — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=-BJrPT7VfEI) |
| [Maintaining The Knee Shield](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/maintain-shield/index.html) † | Begin in knee-shield half guard with upper-body frames. Top removes the shield while staying engaged; bottom keeps that knee between the bodies. Top wins once the shield is cleared. | **R** [Four half-guard passing games — Pearson BJJ](https://www.youtube.com/watch?v=38xCki4sTYY) |
| [Punishing Posts](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/punishing_posts/index.html) † | From knee-shield half guard, bottom forces a hand post and converts it into hip-to-shoulder contact or a two-on-one grip. Top tries to clear the shield and may not flee the engagement. | **R** [Four half-guard passing games — Pearson BJJ](https://www.youtube.com/watch?v=38xCki4sTYY) |
| [Causing Posts](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/causing_posts/index.html) † | From knee-shield half guard, bottom repeatedly forces top’s hands to the mat and keeps them there. Top tries to remove the shield while remaining engaged. Sustain the posts rather than immediately sweeping. | **R** [Four half-guard passing games — Pearson BJJ](https://www.youtube.com/watch?v=38xCki4sTYY) |
| [Ball of Yarn](https://slimemoldgrappling.com/games/guard_games/supine_guard/half_guard/ball_of_yarn/index.html) | From knee-shield half guard, bottom uses legs and frames to deny chest contact and lift top completely clear of the mat. Top tries to clear the shield and establish chest contact, without fleeing. | **R** [Four half-guard passing games — Pearson BJJ](https://www.youtube.com/watch?v=38xCki4sTYY) |

### Guard — Supine / Open Guard (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Create and Break Connections](https://slimemoldgrappling.com/games/guard_games/supine_guard/open_guard/create_and_break_connections/index.html) | Supine bottom begins disconnected from standing top, knees tucked. Bottom builds inside hand/foot connections without sweeping; top clears connections while staying close. Continuous rather than a scored sweep/pass round. | **S** [Foundations/open guard — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=V4QtQTRwwD0) |
| [Maintain Connection](https://slimemoldgrappling.com/games/guard_games/supine_guard/open_guard/maintain_connection/index.html) † | Start supine with one foot already connected to standing top’s leg. Bottom preserves inside hand/foot connections and keeps feet in front; top strips them while staying close. No sweeps; continuous. | **R** [Foundations/open guard — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=V4QtQTRwwD0) |
| [Open Guard Sweeping](https://slimemoldgrappling.com/games/guard_games/supine_guard/open_guard/open_guard_sweeping/index.html) | Supine bottom connects inside and off-balances standing top onto hands or hips. Top clears the feet to reach the knee line. Reset after a fall onto hips; sustain control if hands post. | **S** [Foundations/open guard — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=V4QtQTRwwD0) |

### Guard — Open Guard / Entanglements (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Maintain](https://slimemoldgrappling.com/games/guard_games/supine_guard/open_guard/entanglements/maintain_connection/index.html) | Begin with bottom underneath standing top, legs connected to one or both legs. Bottom retains hip/leg attachment and makes top carry weight; top wins by completely disengaging. | **R** [Leg-entanglement games — Rob Cole](https://www.youtube.com/watch?v=a96BFUXmPO8) |
| [Create](https://slimemoldgrappling.com/games/guard_games/supine_guard/open_guard/entanglements/create_connection/index.html) | Begin seated underneath standing top with attachment to one leg. Bottom upgrades to a leg-and-hip entanglement that restricts movement and transfers weight; top stays upright and wins by disengaging. | **R** [Leg-entanglement games — Rob Cole](https://www.youtube.com/watch?v=a96BFUXmPO8) |
| [Use](https://slimemoldgrappling.com/games/guard_games/supine_guard/open_guard/entanglements/use_connection/index.html) | Start in a leg/hip entanglement beneath standing top. Bottom wins by grounding top’s hands or hips, sustaining hand posts when possible; top wins by disengaging while staying upright. | **R** [Leg-entanglement games — Rob Cole](https://www.youtube.com/watch?v=a96BFUXmPO8) |

### Side Control (10)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Submission Hunting](https://slimemoldgrappling.com/games/side_control/submission_hunting/index.html) | Start chest-to-chest in side control. Top seeks a figure-four arm grip, mounted head-and-arm isolation, or a secure seatbelt on an exposed back. Bottom wins by recovering feet inside or reversing. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Chest-to-Chest Pin Control](https://slimemoldgrappling.com/games/side_control/chext_to_chest_side_control/index.html) | Start flat under a connected chest-to-chest pin. Top maintains contact and secures bent-arm figure-four control; no submissions. Bottom escapes to turtle, seated guard, or full guard; no explosive bridging. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Chest to Chest Pinning](https://slimemoldgrappling.com/games/side_control/maintain_connection/index.html) † | Start chest-to-chest in side control. Top keeps bottom flattened; bottom breaks contact and wins by inserting feet/knees, sitting up, or reversing. Reset on bottom’s escape. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Double Arm Isolation](https://slimemoldgrappling.com/games/side_control/arm_isolation/index.html) | Start flat under side control with top’s hands connected. Top keeps the back down and works toward bent-arm control of both arms, without submissions. Bottom prevents isolation and escapes to turtle or guard. | **R** [Kimura from side control — BJJ Declassified](https://www.youtube.com/watch?v=Q2aN-OiUEw8) |
| [Establish Kesa](https://slimemoldgrappling.com/games/side_control/establish_scarf_hold/index.html) — unfinished template | Unfinished source template: position, objectives, constraints, and wins are blank. Retain as a library backlog item. The video explains scarf-hold positions; it is not a demonstration of a defined site game. | **R** [Full and modified scarf hold — Roy Dean](https://www.youtube.com/watch?v=wcv49O8mQXo) |
| [Maintain Broken Kesa](https://slimemoldgrappling.com/games/side_control/maintain_broken_kesa_gatame/index.html) — unfinished template | Unfinished source template with no playable rules. Retain as a backlog item. The video covers full and modified scarf hold as positional context only. | **R** [Full and modified scarf hold — Roy Dean](https://www.youtube.com/watch?v=wcv49O8mQXo) |
| [Maintain Scarf Hold](https://slimemoldgrappling.com/games/side_control/maintain_scarf_hold/index.html) | Begin in scarf hold, top facing the head with head-and-arm control. Top retains the pin; bottom uses frames and movement to free the head or reverse. Reset after bottom escapes. | **R** [Full and modified scarf hold — Roy Dean](https://www.youtube.com/watch?v=wcv49O8mQXo) |
| [Open Side Control](https://slimemoldgrappling.com/games/side_control/open_side_control/index.html) | Start in side control with chest pressure but no underhook/head control. Top may transition or mount and seeks bent-arm control or a stronger pin; no submissions. Bottom escapes to turtle or guard. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Transition to Mount](https://slimemoldgrappling.com/games/side_control/use_connection/index.html) † | Start chest-to-chest in side control. Top maintains the pin and wins by moving a leg across into mount; bottom wins by inserting knees/feet or reversing. Reset according to the linked source. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Upgrade Kesa](https://slimemoldgrappling.com/games/side_control/upgrade_scarf_hold/index.html) — unfinished template | Unfinished source template: no setup or win condition is supplied. Keep as a backlog item, with the scarf-hold video supplying position context only. | **R** [Full and modified scarf hold — Roy Dean](https://www.youtube.com/watch?v=wcv49O8mQXo) |

### Mount (6)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Wrist Pinning and Trapping](https://slimemoldgrappling.com/games/mount/wrist_pinning_and_trapping/index.html) | Begin in mount. Top pins a wrist beside or across the head, without submissions; bottom keeps hands aimed toward top’s hips and continually frees pinned wrists. No terminal win is specified. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Elbow Exposure Extension Contraction](https://slimemoldgrappling.com/games/mount/elbow_exposure_extension_contraction/index.html) | From mount, top pins a wrist to expose an elbow, then moves the elbow toward the head or inward. No submissions. Bottom destabilizes top and wins by recovering knees in front. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Transitioning to Shoulder Line](https://slimemoldgrappling.com/games/mount/transitioning_to_shoulder_line/index.html) | From mount, top exposes elbows through wrist pins, then slides and turns toward the shoulder line, trapping it between knee and foot. No submissions. Bottom destabilizes top and recovers knees in front. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Low Mount](https://slimemoldgrappling.com/games/mount/low_mount/index.html) † | Start mounted hip-to-hip. Top clears hands, gets under/behind elbows, and wins by joining hands with chest-to-chest or chest-to-back contact. Bottom recovers legs in front and returns seated or standing. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Middle Mount](https://slimemoldgrappling.com/games/mount/middle_mount/index.html) † | Start mounted with top’s hips near bottom’s navel. Top gets under/behind elbows and joins hands with chest contact; bottom creates and occupies space to recover legs in front and sit or stand. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [High Mount](https://slimemoldgrappling.com/games/mount/high_mount/index.html) † | Start with top’s knees in the armpits and hips high toward the chest. Top wins with connected hands and chest contact; bottom recovers legs in front and returns seated or standing. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |

### Back (5)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Maintain and Break Connection](https://slimemoldgrappling.com/games/back/maintain_and_break_connection/index.html) | Start behind turtle with chest-to-back contact. Top follows and retains contact without ever joining their own hands; bottom wins by turning to face top. Reset on the turn. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Shoulder and Hip Control](https://slimemoldgrappling.com/games/back/shoulder_and_hip_control/index.html) | Start behind turtle with a locked waist grip. Top connects to both shoulder and hip lines, retaining back exposure; no hooks or submissions. Bottom wins by turning to face top. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Submission Hunting](https://slimemoldgrappling.com/games/back/submission_hunting/index.html) | Start on the back with a seatbelt and only one hook. Top hunts a submission while maintaining chest contact; no second hook, and close legs only during upper-body attacks. Bottom turns to face. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |
| [Maintain Control](https://slimemoldgrappling.com/games/back/maintain_control/index.html) | Start on the back with seatbelt and both hooks. Top maintains chest-to-back contact without submissions; bottom wins by turning to face top. Reset after bottom succeeds. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [test-back-game](https://slimemoldgrappling.com/games/back/test-back-game/index.html) — test placeholder | Site test entry containing dummy text and no rules. Preserve for catalog completeness and exclude from the playable picker. The back-control reference is contextual only. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |

### Takedowns — Single Leg (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Connection and Movement](https://slimemoldgrappling.com/games/take_downs/single_leg/connection_and_movement/index.html) | Start with one leg held between the attacker’s legs. Attacker maintains and moves the single-leg connection without takedowns; defender balances on the free foot and wins by freeing the captured leg. | **R** [Standing grappling games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=H8L7sI0oYZ4) |
| [Connection and Destabilization](https://slimemoldgrappling.com/games/take_downs/single_leg/connection_and_destabilization/index.html) | Start in a captured single leg. Attacker retains connection and wins by putting the defender onto hands or hips; defender stays balanced and wins by freeing the leg. | **R** [Standing grappling games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=H8L7sI0oYZ4) |
| [Connection, Destabilization, and Hip Access](https://slimemoldgrappling.com/games/take_downs/single_leg/connection_destabilization_and_hip_access/index.html) | Start in a captured single leg. Attacker off-balances to gain hip access while preserving the connection; defender balances and frees the leg. The source prohibits completed takedowns despite the destabilization objective. | **R** [Standing grappling games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=H8L7sI0oYZ4) |

### Takedowns — Hip Throw (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Under the Elbows](https://slimemoldgrappling.com/games/take_downs/hip_throw/under_the_elbows/index.html) † | Start standing in reciprocal underhooks. Both players seek inside position under or behind the elbows. No takedowns; continuous hand-fighting for access. | **R** [No-gi underhooks — Shintaro Higashi](https://www.youtube.com/watch?v=hBgmDRowigQ) |
| [Hip to Hip Connection](https://slimemoldgrappling.com/games/take_downs/hip_throw/hip_to_hip/index.html) † | Start standing with an attacker underhook and a defender overhook. Attacker keeps the underhook and creates hip contact; defender denies that connection. No takedowns or lifts; continuous positional work. | **R** [No-gi underhooks — Shintaro Higashi](https://www.youtube.com/watch?v=hBgmDRowigQ) |
| [Hip to Hip and Elevate](https://slimemoldgrappling.com/games/take_downs/hip_throw/hip_to_hip_and_elevate/index.html) † | Start in the underhook/overhook position. Seek hip contact and lift the partner’s feet clear of the floor; defender denies access and may also elevate. No completed takedowns—only the lift. | **R** [No-gi underhooks — Shintaro Higashi](https://www.youtube.com/watch?v=hBgmDRowigQ) |

### Takedowns — Body Lock and Standing Games (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Connect the Hands](https://slimemoldgrappling.com/games/take_downs/body_lock/connect_the_hands/index.html) | Start standing with reciprocal underhooks. Either player wins by getting around/inside the elbows and joining hands behind the partner’s back. No takedowns; reset after a successful body lock. | **R** [Standing grappling games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=H8L7sI0oYZ4) |
| [Double Underhooks](https://slimemoldgrappling.com/games/take_downs/snap_down/index.html) † | Despite its title, the written game starts disconnected and asks both players to bring the partner’s hands to the mat. No takedowns or explicit terminal win. URL identifies it as a snap-down game. | **R** [Standing grappling games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=H8L7sI0oYZ4) |
| [Knee Tag](https://slimemoldgrappling.com/games/take_downs/knee_tag/index.html) † | Start standing without grips. Attacker scores repeated light touches to either knee; defender uses distance, movement, and limbs to deny touches. No takedowns; continuous. | **R** [Knee Tag — USA Wrestling](https://www.youtube.com/watch?v=WSsl0ImI944) |

### Submissions — Head and Arm Strangle (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Stabilize Front Headlock](https://slimemoldgrappling.com/games/submissions/head_and_arm_strangle/stabilize_front_headlock/index.html) | Start in front headlock with chin-and-elbow control. Top keeps the head covered and hands grounded without submissions; bottom wins by freeing the head. Reset on escape. | **R** [Three front-headlock games — Greg Souders](https://www.youtube.com/watch?v=l4Qz_hz_ZEA) |
| [Capture Head and Arm](https://slimemoldgrappling.com/games/submissions/head_and_arm_strangle/capture_head_and_arm/index.html) | Start over turtle with chin-and-elbow control. Top links the head and one arm, then destabilizes bottom onto their back without submitting. Bottom wins by freeing the head. | **R** [Three front-headlock games — Greg Souders](https://www.youtube.com/watch?v=l4Qz_hz_ZEA) |
| [Finishing](https://slimemoldgrappling.com/games/submissions/head_and_arm_strangle/finishing/index.html) | Begin with chin-and-elbow front-headlock control. Top connects the head and arm, turns bottom onto their back, then secures the finishing grip and submits. Bottom wins by freeing the head. | **R** [Front-strangle games — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=HSWnSITY838) |

### Submissions — Triangle (4)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Causing Posts](https://slimemoldgrappling.com/games/submissions/triangle/causing_posts/index.html) | Start in closed guard. Bottom uses grips plus leg pushes/pulls to make top post; top maintains posture and keeps hands on bottom. No terminal win is specified. | **R** [Triangle — Matt Arroyo](https://www.youtube.com/watch?v=20j7LcZ5xRY) |
| [Maintaining the Finish](https://slimemoldgrappling.com/games/submissions/triangle/maintaining_the_finish/index.html) | Start in a locked triangle configuration. Bottom retains head-and-arm capture; top escapes by making space inside or withdrawing head/arm. Bottom’s task is retention, not a required finish. | **R** [Triangle — Matt Arroyo](https://www.youtube.com/watch?v=20j7LcZ5xRY) |
| [Punishing Posts](https://slimemoldgrappling.com/games/submissions/triangle/punishing_posts/index.html) | Start in closed guard. Bottom forces a post and traps the posting arm with an overhook or underhook; top clears the trap and regains posture. Continuous posture-versus-trap work. | **R** [Triangle — Matt Arroyo](https://www.youtube.com/watch?v=20j7LcZ5xRY) |
| [Arm in Arm Out](https://slimemoldgrappling.com/games/submissions/triangle/arm_in_arm_out/index.html) | Start in closed guard with bottom holding an overhook or underhook. Bottom separates top’s hands and creates one-arm-in/one-arm-out alignment; top fights back to upright posture. | **R** [Triangle — Matt Arroyo](https://www.youtube.com/watch?v=20j7LcZ5xRY) |

### Submissions — Arm Bar (5)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Maintaining the Finish](https://slimemoldgrappling.com/games/submissions/arm_bar/maintaining_the_finish/index.html) | Start in armbar control with the isolated forearm held against the attacker’s chest. Attacker retains the arm without finishing; defender wins by freeing the arm. Reset on escape. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Break their Grip](https://slimemoldgrappling.com/games/submissions/arm_bar/breaking_the_grip/index.html) | Start in armbar position with defender’s hands joined. Attacker maintains elbow control and separates the hands without finishing; defender preserves the grip and escapes. Reset after a successful break or escape. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Hold Them Down](https://slimemoldgrappling.com/games/submissions/arm_bar/hold_them_down/index.html) | Start beside the shoulder with defender’s hands joined above the torso. Attacker holds the shoulder/back down without separating hands or finishing; defender wins by freeing the arm or lifting their back. | **S** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Maintain the Transition](https://slimemoldgrappling.com/games/submissions/arm_bar/maintain_the_transition/index.html) | Start in the S-mount arrangement pictured on the source page. Attacker maintains structure and pins the shoulder without grip breaking or finishing; defender frees the arm or gets their back off the mat. | **S** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |
| [Maintain Arm Isolation](https://slimemoldgrappling.com/games/submissions/arm_bar/maintain_arm_isolation/index.html) | Start mounted with both of bottom’s arms above the head and top’s hands linked underneath. Top preserves the isolation without progressing; bottom wins by recovering both elbows inside or tipping top over. | **R** [Mounted arm-lock — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=n2kfNdH6oo4) |

### Submissions — Leg Locks / Cross Ashi (1)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Maintaining Control](https://slimemoldgrappling.com/games/submissions/leg_locks/cross_ashi/maintaining_control/index.html) | Start in cross ashi/saddle with the outside leg wrapped. Attacker retains or recaptures the foot; defender hides heels and frees the leg. No submissions, finishing pressure, or heel exposure. | **S** [Leglock games — Rob Cole](https://www.youtube.com/watch?v=23vPNbK3NH0&t=158s) |

### Submissions — Rear Naked Choke (6)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Finishing](https://slimemoldgrappling.com/games/submissions/rear_naked_choke/finishing/index.html) | Start with the rear naked choke already assembled and legs around the torso. Attacker increases pressure gradually until a tap; defender taps promptly. Source treats this as brief familiarization, not repeated resistance rounds. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |
| [Maintaining The Finish](https://slimemoldgrappling.com/games/submissions/rear_naked_choke/maintaining_the_finish/index.html) | Start with rear naked choke and leg control assembled. Attacker preserves control without choking or finishing; defender breaks connections and turns to face or hides their back. Reset on escape. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |
| [With One Arm](https://slimemoldgrappling.com/games/submissions/rear_naked_choke/with_one_arm/index.html) | Start on the back with one arm around the neck and legs around the torso. Attacker retains control using only that arm, without finishing or help from the other hand; defender escapes. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |
| [Uncovered Shoulders](https://slimemoldgrappling.com/games/submissions/rear_naked_choke/uncovered_shoulders/index.html) | Start behind the defender with both arms under their armpits and legs around the torso. Attacker upgrades to a secured rear naked choke grip; defender breaks the connections and escapes. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |
| [With Uncovered Hips](https://slimemoldgrappling.com/games/submissions/rear_naked_choke/uncovered_hips/index.html) | Start with the choke grip assembled but no hooks or foot coverage of the hips. Attacker retains control without choking or adding hooks; defender breaks connections and turns to face or hides the back. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |
| [Finishing](https://slimemoldgrappling.com/games/submissions/rear_naked_choke/sub_transition/index.html) — transition to another submission | Submission-transition variant: begin with rear naked choke control. Attacker switches to and finishes a different submission while retaining control; defender turns to face, hides the back, or stands. The starting choke cannot score. | **R** [Rear naked choke — Matt Arroyo](https://www.youtube.com/watch?v=KW2RvtWgBxU) |

### Submissions — Guillotine (4)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Finishing](https://slimemoldgrappling.com/games/submissions/guillotine/finishing/index.html) † | Start in the site’s supine guillotine setup with the partner straddling and head beside the armpit. Bottom slowly adds finishing pressure; top tries to free the head through movement and hand fighting. | **R** [Guillotine — Matt Arroyo](https://www.youtube.com/watch?v=YWwRC0V6O9Y) |
| [Maintaining the Finish](https://slimemoldgrappling.com/games/submissions/guillotine/maintain_the_finish/index.html) † | Use the same supine guillotine setup. Bottom retains neck control without applying the finish; top fights the hands and wins by freeing the head. Reset after escape. | **R** [Guillotine — Matt Arroyo](https://www.youtube.com/watch?v=YWwRC0V6O9Y) |
| [One Arm](https://slimemoldgrappling.com/games/submissions/guillotine/with_one_arm/index.html) † | Use the guillotine setup with only one arm around the neck. Bottom retains control without joining hands or finishing; top fights free of the head control. Reset on escape. | **R** [Guillotine — Matt Arroyo](https://www.youtube.com/watch?v=YWwRC0V6O9Y) |
| [Any Other Submission](https://slimemoldgrappling.com/games/submissions/guillotine/any_other_submission/index.html) | Start in guillotine control. Bottom releases the finishing goal and seeks another submission as top escapes; the initial guillotine cannot score. Top wins by freeing the head and recovering legs inside or standing for three seconds. | **R** [Guillotine — Matt Arroyo](https://www.youtube.com/watch?v=YWwRC0V6O9Y) |

### Submissions — Straight Ankle Lock (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Finishing Mechanics](https://slimemoldgrappling.com/games/submissions/straight_ankle_lock/finishing/index.html) | Start in ashi garami with the ankle wrapped. Attacker applies straight ankle-lock mechanics very slowly; defender taps early. Reset at the tap; use only enough repetitions to recognize the mechanics. | **S** [Straight ankle-lock tips — Dean Lister](https://www.youtube.com/watch?v=rAJ76zkz-Hk) |
| [Maintain Control](https://slimemoldgrappling.com/games/submissions/straight_ankle_lock/maintain_control/index.html) | Start in ashi garami with ankle control. Attacker retains foot and leg; defender hides the heel and frees the leg. No submissions or heel exposure; release completely if the position becomes unsafe. | **R** [Leglock games — Rob Cole](https://www.youtube.com/watch?v=23vPNbK3NH0) |
| [Capture the Foot](https://slimemoldgrappling.com/games/submissions/straight_ankle_lock/capture_the_foot/index.html) | Start in ashi garami with attacker’s outside elbow grounded and the foot not yet secured. Attacker captures the ankle in the armpit and retains it; defender denies capture and frees the leg. No submissions. | **R** [Leglock games — Rob Cole](https://www.youtube.com/watch?v=23vPNbK3NH0) |

### Submissions — Kimura (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Maintain Control](https://slimemoldgrappling.com/games/submissions/twisting_arm_locks/control/index.html) † | Start in side control with a far-arm figure-four grip. Top maintains arm control without finishing; bottom creates space and wins by recovering feet inside or reversing. Release if an escape risks the shoulder. | **R** [Kimura from side control — BJJ Declassified](https://www.youtube.com/watch?v=Q2aN-OiUEw8) |
| [Complete the Grip](https://slimemoldgrappling.com/games/submissions/twisting_arm_locks/complete_the_grip/index.html) | Start in side control with only a wrist grip. Top wins by completing the reinforced figure-four control; bottom wins by recovering feet inside or reversing. Reset after either success. | **R** [Kimura from side control — BJJ Declassified](https://www.youtube.com/watch?v=Q2aN-OiUEw8) |
| [Kimura Bottom Half](https://slimemoldgrappling.com/games/submissions/twisting_arm_locks/dorsal_kimura/index.html) — unfinished template † | Unfinished source template: all setup and task fields are blank. Keep as a backlog item. Georges St-Pierre’s bottom-half-guard kimura video provides related technique context, not missing game rules. | **R** [Bottom-half kimura — Georges St-Pierre](https://www.youtube.com/watch?v=dgYwflmcxKk) |

### Submissions — D’Arce (1)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Maintain Control](https://slimemoldgrappling.com/games/submissions/darce/maintain/index.html) | Start beside a side-lying defender with the D’Arce grip already assembled. Attacker maintains control without finishing; defender hand-fights and turns the hips to free the head. | **R** [D’Arce choke — Stephan Kesting](https://www.youtube.com/watch?v=VOliFfkp5Ik) |

### Pinning / Turtle (11)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Chest to Chest Chest to Back](https://slimemoldgrappling.com/games/pinning/chest_to_chest_chest_to_back/index.html) | Start with top’s arms around bottom’s waist. Top clears hands, gets under/behind elbows, and wins with joined hands plus chest-to-chest/back contact. Bottom recovers legs in front and returns seated or standing. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Initiating Maintaining Chest to Back Contact](https://slimemoldgrappling.com/games/pinning/initiating_maintaining_chest_to_back_contact/index.html) | Begin with waist control behind a partner facing away. Top follows chest-to-back, switching to connected chest-to-chest control if the back is hidden. Bottom turns to face, recovers legs in front, and sits or stands. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Covering the Hips](https://slimemoldgrappling.com/games/pinning/covering_the_hips/index.html) | Alternate starts facing toward/away with a locked waist grip. Top adds hip coverage to chest contact; bottom turns, recovers legs in front, and returns seated or standing. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Covering the Shoulders](https://slimemoldgrappling.com/games/pinning/cover_the_head_and_shoulders/index.html) — cover and follow | Cover-and-follow variant: top starts chest over turtle’s shoulder blades and keeps head/shoulders covered. Bottom breaks that connection by attaching to the legs, winning by exiting into a leg entanglement. | **R** [Three front-headlock games — Greg Souders](https://www.youtube.com/watch?v=l4Qz_hz_ZEA) |
| [Covering the Shoulders](https://slimemoldgrappling.com/games/pinning/cracking_the_egg/index.html) — break down / cracking the egg † | Breakdown variant, also titled Covering the Shoulders: top starts over turtle and grounds hips/shoulders or progresses behind with hooks. Bottom wins by standing or putting legs between the bodies. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Attacking Turtle Arms](https://slimemoldgrappling.com/games/pinning/turtle_arm_attack/index.html) — arm control | Arm-control variant: start beside turtle with one hand across the back and control of an arm. Top breaks bottom onto hips/shoulders with chest contact; bottom stands or brings legs inside. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Attacking Turtle Arms](https://slimemoldgrappling.com/games/pinning/turtle_with_post_control/index.html) — post control | Post-control variant: start beside turtle controlling a point of support. Top breaks bottom onto hips/shoulders with chest contact and joined hands; bottom stands or brings legs between the bodies. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Turtle Body Lock](https://slimemoldgrappling.com/games/pinning/turtle_body_lock/index.html) † | Start with top chest-to-back over turtle and a locked body grip. Top keeps head covered and hands grounded without submissions; bottom attacks leg connections to stand or recover legs inside. | **R** [Passing and pinning — Standard Jiu-Jitsu](https://www.youtube.com/watch?v=Ps3nesZp1YU) |
| [Front Headlock to the Back](https://slimemoldgrappling.com/games/pinning/front_headlock_to_back/index.html) † | Begin in chin-and-elbow front headlock. Top controls head and posts while moving behind to chest-to-back contact, without submissions. Bottom wins by standing or getting feet between the bodies. | **R** [Three front-headlock games — Greg Souders](https://www.youtube.com/watch?v=l4Qz_hz_ZEA) |
| [Isolating the Neck](https://slimemoldgrappling.com/games/pinning/isolate_the_neck/index.html) † | Begin in chin-and-elbow front headlock. Top wins by linking hands around only the neck, without submissions; bottom separates the hands and wins by standing or recovering feet inside. | **R** [Three front-headlock games — Greg Souders](https://www.youtube.com/watch?v=l4Qz_hz_ZEA) |
| [Turtle Ankle Attacks](https://slimemoldgrappling.com/games/pinning/turtle_ankle_attacks/index.html) † | Start chest-to-back over turtle with a locked body grip. Top uses ankle control to pin hips or shoulders, without submissions; bottom attacks the legs to stand or recover legs inside. | **R** [Scrambling system — Rob Cole](https://www.youtube.com/watch?v=GsaDeiRO7s8) |

### Knee On Belly (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [No Hands](https://slimemoldgrappling.com/games/knee_on_belly/no_hands/index.html) † | Start in knee-on-belly with the free leg extended. Top balances and may switch sides but cannot use hands on partner or mat. Bottom removes the knee or reverses to win. | **R** [Knee-on-stomach concepts — Jean Jacques Machado](https://www.youtube.com/watch?v=sSmjbsEa2gA) |
| [Maintain Position](https://slimemoldgrappling.com/games/knee_on_belly/maintain_position/index.html) | Start in knee-on-belly with upper-body hand connections. Top retains the pin; bottom blocks the knee and moves clear of it. Reset once the knee no longer pins the torso. | **R** [Knee-on-stomach concepts — Jean Jacques Machado](https://www.youtube.com/watch?v=sSmjbsEa2gA) |
| [Knee On Belly Attacks](https://slimemoldgrappling.com/games/knee_on_belly/kob_attacks/index.html) | Start in knee-on-belly. Top isolates an arm or transitions to another available submission and wins by a tap; bottom removes the pin or reverses. Reset after either success. | **R** [Knee-on-stomach concepts — Jean Jacques Machado](https://www.youtube.com/watch?v=sSmjbsEa2gA) |

### North South (3)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Arms Out](https://slimemoldgrappling.com/games/north_south/maintain_arms_out_pin/index.html) † | Start north-south with top’s arms under bottom’s arms. Top maintains chest pressure and a flat pin; bottom wins by recovering feet/knees inside, standing, or reversing. | **R** [North-south control — RVV BJJ](https://www.youtube.com/watch?v=cans383if9Q) |
| [Transition](https://slimemoldgrappling.com/games/north_south/use_connection/index.html) † | Start chest-to-chest in side control. Top transitions to north-south or the opposite side and holds for three seconds; bottom inserts knees/feet or reverses to win. | **R** [North-south control — RVV BJJ](https://www.youtube.com/watch?v=cans383if9Q) |
| [North South Pinning](https://slimemoldgrappling.com/games/north_south/maintain_the_pin/index.html) † | Start north-south with top’s elbows in bottom’s armpits. Top retains chest contact and flat shoulders; bottom creates space, recovers knees/feet inside, stands, or reverses. | **R** [North-south control — RVV BJJ](https://www.youtube.com/watch?v=cans383if9Q) |

### Scrambles (4)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Ankle Wars](https://slimemoldgrappling.com/games/scrambles/ankle_wars/index.html) | Both begin on all fours holding the other’s far ankle. Scramble on top with ankle/knee control, lifting that support from the mat for two seconds while clearing the opponent’s grip on your own leg. | **S** [Scrambling system — Rob Cole](https://www.youtube.com/watch?v=GsaDeiRO7s8) |
| [Back-to-Back Spin Up](https://slimemoldgrappling.com/games/scrambles/spin_up/index.html) | Start seated back-to-back. Stay connected through the transition and come on top with an ankle/knee lifted and controlled for two seconds, while freeing yourself from the opponent’s connection. | **S** [Scrambling system — Rob Cole](https://www.youtube.com/watch?v=GsaDeiRO7s8) |
| [Creative Scramble Starts](https://slimemoldgrappling.com/games/scrambles/creative_starts/index.html) | Choose a connected start such as belly-down, inverted, or seated. No submissions or disengagement. Win by coming on top with the partner’s knee/ankle lifted and controlled for two seconds. | **S** [Scrambling system — Rob Cole](https://www.youtube.com/watch?v=GsaDeiRO7s8) |
| [No Knees Top Player](https://slimemoldgrappling.com/games/scrambles/no_knees/index.html) | Begin from a top/bottom ground position. Top stays above without kneeling, locking hands, or submitting; bottom controls knees/ankles to stand or come on top. The source’s standing objective and formal win differ. | **S** [Scrambling system — Rob Cole](https://www.youtube.com/watch?v=GsaDeiRO7s8) |

### Striking (5)

| Game / source | Setup, task, and win or reset | YouTube reference |
| --- | --- | --- |
| [Belly Tag](https://slimemoldgrappling.com/games/striking/belly_tag/index.html) | Both start in the same stance. Attacker lightly tags the belly with the pad of the lead foot; defender intercepts or evades while maintaining stance. Keep the game moving. | **R** [Ecological introduction to MMA — SBG Scarborough](https://www.youtube.com/watch?v=wXDHoh3zyc8) |
| [Belly and Forehead Tag](https://slimemoldgrappling.com/games/striking/belly_forehead_tag/index.html) | From matching stances, tag belly with the lead foot or forehead with a straight lead hand. Defender intercepts and evades. Light touches only; the source permits substituting a shoulder target. | **R** [Ecological introduction to MMA — SBG Scarborough](https://www.youtube.com/watch?v=wXDHoh3zyc8) |
| [Belly and Forehead Tag + Stance Switching](https://slimemoldgrappling.com/games/striking/belly_forehead_tag_with_stance_switch/index.html) | Use belly-foot and forehead-hand targets while allowing stance switches. Score a controlled touch while managing distance and balance; defender moves and intercepts through the stance changes. | **R** [Ecological introduction to MMA — SBG Scarborough](https://www.youtube.com/watch?v=wXDHoh3zyc8) |
| [Belly Tag + Laces to Back of Leg](https://slimemoldgrappling.com/games/striking/belly_tag_laces_to_leg/index.html) | From matching stances, tag belly with the lead foot or the back of the lead leg with laces/shin. Defender intercepts with hands/legs and uses shin orientation to protect the leg. | **R** [Ecological introduction to MMA — SBG Scarborough](https://www.youtube.com/watch?v=wXDHoh3zyc8) |
| [Belly, Forehead, and Laces Tag](https://slimemoldgrappling.com/games/striking/belly_forehead_laces/index.html) | Use all three targets: belly with foot, forehead with lead hand, and back of lead leg with laces/shin. Attacker makes clean, light tags; defender manages spacing and interceptions. | **R** [Ecological introduction to MMA — SBG Scarborough](https://www.youtube.com/watch?v=wXDHoh3zyc8) |

### Source issues to resolve before app import

- **Unfinished templates:** Establish Kesa, Maintain Broken Kesa, Upgrade Kesa, and Kimura Bottom Half have blank rule fields. The back test entry has dummy text. Their videos provide context only.
- **Misleading title:** Double Underhooks describes a hands-to-mat task and uses a snap-down URL; preserve the original title for traceability and review its app display name.
- **Conflicting outcomes:** Seated Guard / Destabilization describes a chest-contact objective but a leg-connection win for bottom. No Knees Top Player describes standing as bottom's objective but lists a top-position win. Several pages also refer to resets despite listing no terminal win. Do not invent scoring to fill those gaps.
- **Visual starting position:** Maintain the Transition refers to an S-mount picture on its source page; retain that image reference or the source-linked video when building the app entry.
- **Curriculum:** The site's [lesson plans](https://slimemoldgrappling.com/lesson_plans/index.html) organize games into progressions and sometimes rename them. This inventory counts standalone entries in the Games catalog; lesson-plan repetitions are not additional catalog entries.

## 17. Useful references

- [Streamlit documentation](https://docs.streamlit.io/)
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [pytest documentation](https://docs.pytest.org/)

---

*Merged from the original BJJ app idea and OpenMat project-planning notes on October 21, 2026. This note preserves the full Slime Mold research catalog and the development plan. It is a planning document, not evidence that features have been built or validated.*

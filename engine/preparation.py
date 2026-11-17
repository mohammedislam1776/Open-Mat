"""Proposed templates transcribed/adapted from the supplied project notes."""
import json
from pathlib import Path
from .recommender import REHEARSAL_CUES, POSITION_LABELS

NOTICE = 'Proposed routine pending coach and physiotherapist review. Not a validated BJJ injury-prevention protocol. Finish warm and coordinated, without fatigue. Completion is not clearance to roll.'
CAUTION = 'Use comfortable ranges. Stop for sharp pain, instability, numbness, or dizziness. Follow existing clinician restrictions; recent injury, surgery, recurrent dislocation, or ongoing symptoms need an individualized plan. No neck bridges, headstands, or forced stretching.'


def load_exercises():
    return json.loads((Path(__file__).resolve().parents[1] / 'data/preparation.json').read_text())


def make_routine(kind, minutes, priorities, equipment='none', excluded=(), standing=False, position_preferences=None):
    library={e['id']:e for e in load_exercises()}
    if kind != 'warm_up':
        raise ValueError('Only warm-up routines are supported.')
    lengths={5:[2,1,0,2],10:[3,2,2,3],15:[4,4,3,4],20:[5,5,4,6],25:[7,5,4,9]}[minutes]
    activation=['bridge','scapula','bird','balance'] if equipment=='none' else ['band_steps','band_rotation','bird','balance']
    if minutes <= 10:
        activation = activation[:1] + ['balance']
    mobility = ['ankles','hands'] if minutes == 5 else ['ankles','hinge','hands'] if minutes == 10 else ['ankles','hinge','adductor','rotation','hands']
    phases=[('Raise temperature','general',['movement']),('Dynamic mobility','mobility',mobility),('Light activation','activation',activation),('Grappling-specific ramp','rehearsal',['ground_rehearsal'])]
    steps=[]; elapsed=0
    for (title,stage,ids),length in zip(phases,lengths):
        if not length:
            continue
        exercises=[dict(library[i]) for i in ids if i not in excluded]
        if minutes == 5 and stage == 'mobility':
            for exercise in exercises:
                exercise['dose']='About 30 seconds of easy movement; choose comfortable range.'
        if stage=='comfort' and length==1 and exercises:
            exercises[0]['dose']='Choose one comfortable movement; if stretching, about 20 seconds per side. Use the remaining time to transition.'
        instructions='Use the phase as an easy time window, not a repetition target. Leave time for rest and transitions; do not rush to complete every movement.'
        if stage=='rehearsal':
            movement = 'familiar stance movement and entries, with previously learned, coached breakfalls only' if standing else 'familiar ground movement'
            if standing and any(p != 'takedowns' for p in priorities):
                movement += ' plus comfortable transitions for the selected ground positions'
            if 'ground_rehearsal' in excluded and not standing:
                movement = 'your existing comfortable, approved preparation; the ground-transition sequence is excluded'
            if standing:
                exercises = []
            focus_cues = '; '.join((f"{POSITION_LABELS[position_preferences[p]]}: rehearse the selected games’ starts and tasks cooperatively, without changing position" if position_preferences and position_preferences.get(p) else REHEARSAL_CUES[p]) for p in priorities)
            instructions=f"Divide this phase into three easy parts: {movement}; cooperative rehearsal of {', '.join(p.replace('_',' ') for p in priorities)} ({focus_cues}); then a simple positional task with gradually increasing resistance and no submission finishes. Skip excluded or unfamiliar movements. Put bands away before partner work."
        elif not exercises:
            instructions='All movements in this phase are excluded. Use the time for rest or your existing clinician-approved preparation; OpenMat will not invent a replacement.'
        steps.append(dict(title=title,stage=stage,start=elapsed,end=elapsed+length,minutes=length,instructions=instructions,exercises=exercises))
        elapsed+=length
    return dict(steps=steps,notice=NOTICE + (' Short preparation: use fewer easy movements and increase effort gradually; add time or reduce training intensity if you are not ready.' if minutes <= 10 else ''),caution=CAUTION,aftercare='')

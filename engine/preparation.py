"""Proposed templates transcribed/adapted from the supplied project notes."""
import json
from pathlib import Path

NOTICE = 'Proposed routine pending coach and physiotherapist review. Not a validated BJJ injury-prevention protocol. Finish warm and coordinated, without fatigue. Completion is not clearance to roll.'
CAUTION = 'Use comfortable ranges. Stop for sharp pain, instability, numbness, or dizziness. Follow existing clinician restrictions; recent injury, surgery, recurrent dislocation, or ongoing symptoms need an individualized plan. No neck bridges, headstands, or forced stretching.'


def load_exercises():
    return json.loads((Path(__file__).resolve().parents[1] / 'data/preparation.json').read_text())


def make_routine(kind, minutes, priorities, equipment='none', excluded=(), standing=False):
    library={e['id']:e for e in load_exercises()}
    if kind=='warm_up':
        lengths={15:[4,4,3,4],20:[5,5,4,6],25:[7,5,4,9]}[minutes]
        activation=['bridge','scapula','bird','balance'] if equipment=='none' else ['band_steps','band_rotation','bird','balance']
        phases=[('Raise temperature','general',['movement']),('Dynamic mobility','mobility',['ankles','hinge','adductor','rotation','hands']),('Light activation','activation',activation),('Grappling-specific ramp','rehearsal',['ground_rehearsal'])]
    else:
        lengths={5:[2,1,1,1],10:[3,3,2,2],15:[5,4,3,3]}[minutes]
        phases=[('Lower activity gradually','settle',['walk']),('Comfortable mobility','comfort',['stretch']),('Relaxed breathing and body check','check',['breathe']),('Optional reflection','reflection',['reflect'])]
    steps=[]; elapsed=0
    for (title,stage,ids),length in zip(phases,lengths):
        exercises=[dict(library[i]) for i in ids if i not in excluded]
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
            instructions=f"Divide this phase into three easy parts: {movement}; cooperative rehearsal of {', '.join(p.replace('_',' ') for p in priorities)}; then a simple positional task with gradually increasing resistance and no submission finishes. Skip excluded or unfamiliar movements. Put bands away before partner work."
        elif not exercises:
            instructions='All movements in this phase are excluded. Use the time for rest or your existing clinician-approved preparation; OpenMat will not invent a replacement.'
        steps.append(dict(title=title,stage=stage,start=elapsed,end=elapsed+length,minutes=length,instructions=instructions,exercises=exercises))
        elapsed+=length
    return dict(steps=steps,notice=NOTICE if kind=='warm_up' else 'Wrap up for a gradual transition, comfort, and reflection. No promise of preventing injury or next-day soreness.',caution=CAUTION,aftercare='' if kind=='warm_up' else 'Afterward, rehydrate, eat according to normal needs, change damp training clothes, and follow gym hygiene practices. New or persistent symptoms should change subsequent training and prompt appropriate assessment.')

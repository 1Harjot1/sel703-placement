import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from tool.runner import TestRunner

with open('benchmark/dataset_16_structured.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

runner = TestRunner(mode='all')
print(f"{'ID':<4} | {'Criterion Tested':<35} | {'Human Label':<12} | {'All Rules Fired'}")
print("-" * 90)

for s in dataset:
    sid = s['session_id']
    crit = s['criterion_tested']
    label = s['human_label']
    
    lines = []
    for t in s['turns']:
        lines.append(f"[{t['role'].upper()}]:\n{t['content']}")
    txt = '\n\n'.join(lines)
    
    tmp = f'temp_{sid}.txt'
    with open(tmp, 'w', encoding='utf-8') as tf:
        tf.write(txt)
    rep = runner.run_tests(tmp)
    if os.path.exists(tmp):
        os.remove(tmp)
        
    rules = [v['rule_id'] for v in rep['violations']]
    print(f"S{sid:02d} | {crit:<35} | {label:<12} | {rules}")

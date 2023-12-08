import json
import numpy as np
from collections import Counter

with open('./Data/BioASQ-task11bPhaseB-testset3.json') as f:
    data_test = json.load(f)

with open('./Results/BioASQform_BioASQ-answer_factoid_combined_combine.json') as f:
    data_factoid = json.load(f)

with open('./Results/list_combine_list_30_combine.json') as f:
    data_list = json.load(f)

#data_yesno = []
with open('./Results/BioASQform_BioASQ-answer_yesno_combined.json', 'r') as f:
    data_yesno = json.load(f)
    #for line in f:
    #    d = json.loads(line)
    #    data_yesno.append(d)

'''
dataa = {}
for q in data_yesno:
    id = q['id'].split('_')[0]
    if id in dataa:
        dataa[id].append(q['label'])
    else:
        dataa[id] = [q['label']]

for r in dataa.items():
    id = r[0]
    counts = Counter(r[1])
    if 'yes' not in counts:
        dataa[id] = 'no'
    elif 'no' not in counts:
        dataa[id] = 'yes'
    else:
        if counts['yes'] > counts['no']:
            dataa[id] = 'yes'
        elif counts['no'] > counts['yes']:
            dataa[id] = 'no'
        else:
            dataa[id] = 'yes'
'''
for q in data_test['questions']:
    if q['type'] == 'yesno':
        #q['exact_answer'] = dataa[q['id']]
        for q_yesno in data_yesno['questions']:
            if q['id'] == q_yesno['id']:
                q['exact_answer'] = q_yesno['exact_answer']
    elif q['type'] == 'factoid':
        for q_fact in data_factoid['questions']:
            if q['id'] == q_fact['id']:
                q['exact_answer'] = q_fact['exact_answer']
    elif q['type'] == 'list':
        for q_list in data_list['questions']:
            if q['id'] == q_list['id']:
                q['exact_answer'] = q_list['exact_answer']

with open('./Results/bioasq-testset3-whole.json') as f:
    data_ideal = json.load(f)

for q_exact in data_test['questions']:
    for q_ideal in data_ideal['questions']:
        if q_exact['id'] == q_ideal['id']:
            q_exact['ideal_answer'] = q_ideal['ideal_answer']

with open('./bioasq_11b_biobert_processed_factoid.json', 'w') as f:
    f.write(json.dumps(data_test,indent=4))
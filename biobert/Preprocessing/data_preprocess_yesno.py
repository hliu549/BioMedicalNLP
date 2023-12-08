import json
import numpy as np


with open('/Users/sanjana/Desktop/BioASQ_11b/BioASQ-task11bPhaseB-testset3.json') as f:
    data_test = json.load(f)

#with open('/Users/sanjana/Desktop/BioASQ_11b/training11b.json') as f:
#    data_train = json.load(f)

#new_data_train = {"data" : [{"paragraphs" : []}]}
new_data_test = {"data" : [{"paragraphs" : []}]}
'''
for q in data_train['questions']:
    if q['type'] == 'yesno':
        i = 1

        for s in q['snippets']:
            new_qas = {"qas" : [], "context" : ""}

            if q['exact_answer']=="yes":
                new_qas['qas'].append(
                    {
                    "id" : q['id'] + "_" + "{:03d}".format(i),
                    "question" : q['body'],
                    "is_impossible" : False,
                    "answers" : q['exact_answer']
                    }
                )
            else:
                new_qas['qas'].append(
                    {
                    "id" : q['id'] + "_" + "{:03d}".format(i),
                    "question" : q['body'],
                    "is_impossible" : True,
                    "answers" : q['exact_answer']
                    }
                )
            new_qas['context'] = s['text']
            new_data_train['data'][0]['paragraphs'].append(new_qas)

            i += 1
'''

for q in data_test['questions']:
    if q['type'] == 'yesno':
        i = 1
        for s in q['snippets']:
            new_qas = {"qas" : [], "context" : ""}

            new_qas['qas'].append(
                {
                "id" : q['id'] + "_" + "{:03d}".format(i),
                "question" : q['body']
                }
            )
            new_qas['context'] = s['text']
            new_data_test['data'][0]['paragraphs'].append(new_qas)

            i += 1

#preprocessed_data_train = json.dumps(new_data_train)
preprocessed_data_test = json.dumps(new_data_test)

#with open('/Users/sanjana/Desktop/BioASQ_11b/bioasq_11b_train_yesno.json', 'w') as f:
#    f.write(preprocessed_data_train)

with open('/Users/sanjana/Desktop/BioASQ_11b/bioasq_11b_test3_yesno.json', 'w') as f:
    f.write(preprocessed_data_test)

'''
for q in data_test['questions']:
    if "triples" not in q:
        q["triples"] = []
    if "concepts" not in q:
        q["concepts"] = []
    if q["type"] == "factoid":
        q["exact_answer"] = [[q["exact_answer"][0]]]

preprocessed_data = json.dumps(data_test)

with open('bioasq_11b_golden.json', 'w') as f:
    f.write(preprocessed_data)
'''

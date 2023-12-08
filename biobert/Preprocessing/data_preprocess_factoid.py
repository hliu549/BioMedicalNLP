import json
import numpy as np

def getIndexInText(text, answer):
    return text.find(answer)

with open('/Users/sanjana/Desktop/BioASQ_11b/BioASQ-task11bPhaseB-testset3.json') as f:
    data_test = json.load(f)

#with open('/Users/sanjana/Desktop/BioASQ_11b/training11b.json') as f:
#    data_train = json.load(f)

#new_data_train = {"data" : [{"paragraphs" : [], "title": "BioASQ8b"}], "version": "BioASQ8b"}
new_data_test = {"data" : [{"paragraphs" : [], "title": "BioASQ8b"}], "version": "BioASQ8b"}
'''
for q in data_train['questions']:
    if q['type'] == 'factoid':
        i = 1
        for s in q['snippets']:
            for e in q['exact_answer']:
                new_qas = {"qas" : [], "context" : ""}
                start_index = getIndexInText(s['text'], e)
                if start_index == -1:
                    continue
                else:
                    new_qas['qas'].append(
                        {
                        "id" : q['id'] + "_" + "{:03d}".format(i),
                        "question" : q['body'],
                        "answers" : [{"text": e,
                                    "answer_start" : start_index}]
                        }
                    )
                
                new_qas['context'] = s['text']
                new_data_train['data'][0]['paragraphs'].append(new_qas)

                i += 1
'''
for q in data_test['questions']:
    if q['type'] == 'factoid':
        i = 1
        for s in q['snippets']:
            new_qas = {"qas" : [], "context" : ""}
            new_qas['qas'].append(
                {
                "id" : q['id'] + "_" + "{:03d}".format(i),
                "question" : q['body'],
                "answers" : []
                }
            )
            new_qas['context'] = s['text']
            new_data_test['data'][0]['paragraphs'].append(new_qas)

            i += 1

#preprocessed_data_train = json.dumps(new_data_train)
preprocessed_data_test = json.dumps(new_data_test)

#with open('/Users/sanjana/Desktop/BioASQ_11b/bioasq_11b_train_factoid.json', 'w') as f:
#    f.write(preprocessed_data_train)

with open('/Users/sanjana/Desktop/BioASQ_11b/bioasq_11b_test3_factoid.json', 'w') as f:
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

with open('/Users/sanjana/Desktop/BioASQ_11b/Train Test Data/bioasq_11b_golden.json', 'w') as f:
    f.write(preprocessed_data)
'''

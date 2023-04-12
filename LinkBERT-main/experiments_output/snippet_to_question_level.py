import sys
import json


test_output_path = sys.argv[1]
save_path = sys.argv[2]

with open(test_output_path, 'r') as f:
    test_outputs = json.load(f)

y_pred = {}
for i in test_outputs:
    preds = test_outputs[i]
    pred = {}
    for j in preds:
        ans = j['text'].lower().strip()
        if ans not in pred:
            pred[ans] = 0
        else:
            pred[ans] += j['probability']
    sorted_d = sorted(pred.items(), key=lambda x: x[1], reverse=True)
    top_5_keys = [[key] for key, value in sorted_d[:5]]
    
    y_pred[i.split("_")[0]] = top_5_keys

question_list = []
for q in y_pred:
    question_list.append({"id":q, "type":"factoid", "exact_answer":y_pred[q]})

result = {"questions":question_list}

with open(save_path, "w") as outfile:
    json.dump(result, outfile)
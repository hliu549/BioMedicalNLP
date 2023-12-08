""" MetaMap interactive using embedded string """
import argparse
import re
import json
import jsonlines

if __name__ == '__main__':

    # got this using the MetaMap tool from NIH website after obtaining UMLS License
    with open('./text.out') as f:
        content = f.read()

    metaphrases = []

    pattern1 = re.compile(r'>>>>> MMI(.*?)<<<<< MMI', re.DOTALL)
    matches = pattern1.findall(content)
    for m in matches:
        pattern2 = re.compile(r'-tx-1-(.*?)"-')
        ms = list(set(pattern2.findall(m)))
        metaphrases.append([match[1:] for match in ms])

    with open('./11b_yesno_train.json') as f:
        data_train = json.load(f)

    questions = data_train["questions"]
    #with open('batch_input.txt', mode = 'a') as f_inp:
    with jsonlines.open('./output.jsonl', mode='a') as writer:
        i = 0
        for q in questions:
            if q["type"] == "yesno":
                #f_inp.write(q["body"]+ '\n')
                
                final_json = {}
                final_json["question"] = q["body"]
                final_json["answer"] = q["exact_answer"]
                final_json["meta_info"] = "step1"
                final_json["options"] = {"A": "yes", "B": "no"}
                final_json["answer_idx"] = "A" if q["exact_answer"] == "yes" else "B"
                
                final_json["metamap_phrases"] = metaphrases[i]
                writer.write(final_json)

                i += 1
                
    



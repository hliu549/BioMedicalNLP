import json
import sys


data_path = sys.argv[1]

data = []

with open(data_path, 'r') as f:

    for line in f:

        content = json.loads(line)

        new_content = {}
        new_content['id'] = content['qas'][0]['id']
        new_content['question'] = content['qas'][0]['question']
        new_content['context'] = content['context']
        answer_start = []
        text = []
        answers = content['qas'][0]['answers']
        for answer in answers:
            answer_start.append(answer['answer_start'])
            text.append(answer['text'])
        new_content['answers'] = {'answer_start':answer_start, 'text':text}

        data.append(new_content)


with open(data_path, 'w') as f:
        
        for item in data:
            
            json.dump(item, f)
            f.write('\n')

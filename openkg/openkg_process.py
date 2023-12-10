import pandas as pd
import json

with open('data.json') as file:
    data = json.load(file)
graphs = data['@graph']

class_id_map = {}
for graph in graphs:
    class_id_map[graph['@id'].lower().strip()] = graph['label']['@value'].lower().strip()

entity2id, relationp2id = {}, {}
triples = []

for graph in graphs:
    ent1 = graph['label']['@value'].lower().strip()
    if ent1 not in entity2id:
        entity2id[ent1] = len(entity2id)
    for k in graph:
        if '@' in k or 'label' in k: # k is not a relationship
            continue
        # fill entity2id
        s = graph[k].replace(';', ',')
        ent2s = s.split(',')
        for entity in ent2s:
            if entity.lower().strip() in class_id_map:
                ent2 = class_id_map[entity.lower().strip()]
            else:
                ent2 = entity.lower().strip()
            if ent2 not in entity2id:
                entity2id[ent2] = len(entity2id)
            # fill relationship2id
            if k not in relationp2id:
                relationp2id[k] = len(relationp2id)
            # create train tuple
            triples.append((entity2id[ent1], entity2id[ent2], relationp2id[k]))

print('Total entities: ', len(entity2id))
print('Total relationships: ', len(relationp2id))        
print('Total training triples: ', len(triples))

with open("train2id.txt", "w") as f:
    f.write(f"{len(triples)}\n")
    for (left, right, relation) in triples:
        f.write(f"{left}\t{right}\t{relation}\n")

with open("relation2id.txt", "w") as f:
    f.write(f"{len(relationp2id)}\n")
    for k, v in relationp2id.items():
        f.write(f"{k}\t{v}\n")

with open("entity2id.txt", "w") as f:
        f.write(f"{len(entity2id)}\n")
        for k, v in entity2id.items():
            f.write(f"{k}\t{v}\n")
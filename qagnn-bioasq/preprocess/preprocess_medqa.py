import os
import json
import pickle
import numpy as np
from tqdm import tqdm
from collections import defaultdict

for fname in ["test"]:
    with open(f"./data/bioasq/output_{fname}.jsonl") as f:
        lines = f.readlines()
    examples = []
    for i in tqdm(range(len(lines))):
        line = json.loads(lines[i])
        _id  = f"train-{i:05d}"
        answerKey = line["answer_idx"]
        stem      = line["question"]
        choices   = [{"label": k, "text": line["options"][k]} for k in "AB"]
        stmts     = [{"statement": stem +" "+ c["text"]} for c in choices]
        ex_obj    = {"id": _id,
                     "question": {"stem": stem, "choices": choices},
                     "answerKey": answerKey,
                     "statements": stmts
                    }
        examples.append(ex_obj)
    with open(f"./data/bioasq/statement/{fname}.statement.jsonl", 'w') as fout:
        for dic in examples:
            print (json.dumps(dic), file=fout)

#Load scispacy entity linker
import spacy
import scispacy
from scispacy.linking import EntityLinker

def load_entity_linker(threshold=0.90):
    nlp = spacy.load("en_core_web_sm")
    linker = EntityLinker(
        resolve_abbreviations=True,
        name="umls",
        threshold=threshold)
    nlp.add_pipe(linker)
    return nlp, linker

nlp, linker = load_entity_linker()

def entity_linking_to_umls(sentence, nlp, linker):
    doc = nlp(sentence)
    entities = doc.ents
    all_entities_results = []
    for mm in range(len(entities)):
        entity_text = entities[mm].text
        entity_start = entities[mm].start
        entity_end = entities[mm].end
        all_linked_entities = entities[mm]._.kb_ents
        all_entity_results = []
        for ii in range(len(all_linked_entities)):
            curr_concept_id = all_linked_entities[ii][0]
            curr_score = all_linked_entities[ii][1]
            curr_scispacy_entity = linker.kb.cui_to_entity[all_linked_entities[ii][0]]
            curr_canonical_name = curr_scispacy_entity.canonical_name
            curr_TUIs = curr_scispacy_entity.types
            curr_entity_result = {"Canonical Name": curr_canonical_name, "Concept ID": curr_concept_id,
                                  "TUIs": curr_TUIs, "Score": curr_score}
            all_entity_results.append(curr_entity_result)
        curr_entities_result = {"text": entity_text, "start": entity_start, "end": entity_end,
                                "start_char": entities[mm].start_char, "end_char": entities[mm].end_char,
                                "linking_results": all_entity_results}
        all_entities_results.append(curr_entities_result)
    return all_entities_results

#Run entity linking to UMLS for all questions
def process(input):
    nlp, linker = load_entity_linker()
    stmts = input
    for stmt in tqdm(stmts):
        stem = stmt['question']['stem']
        stem = stem[:3500]
        stmt['question']['stem_ents'] = entity_linking_to_umls(stem, nlp, linker)
        for ii, choice in enumerate(stmt['question']['choices']):
            text = stmt['question']['choices'][ii]['text']
            stmt['question']['choices'][ii]['text_ents'] = entity_linking_to_umls(text, nlp, linker)
    return stmts

for fname in ["test"]:
    with open(f"./data/bioasq/statement/{fname}.statement.jsonl") as fin:
        stmts = [json.loads(line) for line in fin]
        res = process(stmts)
    with open(f"./data/bioasq/statement/{fname}.statement.umls_linked.jsonl", 'w') as fout:
        for dic in res:
            print (json.dumps(dic), file=fout)

#Convert UMLS entity linking to DDB entity linking (our KG)
umls_to_ddb = {}
with open('./data/ddb/ddb_to_umls_cui.txt') as f:
    for line in f.readlines()[1:]:
        elms = line.split("\t")
        umls_to_ddb[elms[2]] = elms[1]

def map_to_ddb(ent_obj):
    res = []
    for ent_cand in ent_obj['linking_results']:
        CUI  = ent_cand['Concept ID']
        name = ent_cand['Canonical Name']
        if CUI in umls_to_ddb:
            ddb_cid = umls_to_ddb[CUI]
            res.append((ddb_cid, name))
    return res

def process_ddb(fname):
    with open(f"./data/bioasq/statement/{fname}.statement.umls_linked.jsonl") as fin:
        stmts = [json.loads(line) for line in fin]
    with open(f"./data/bioasq/grounded/{fname}.grounded.jsonl", 'w') as fout:
        for stmt in tqdm(stmts):
            sent = stmt['question']['stem']
            qc = []
            qc_names = []
            for ent_obj in stmt['question']['stem_ents']:
                res = map_to_ddb(ent_obj)
                for elm in res:
                    ddb_cid, name = elm
                    qc.append(ddb_cid)
                    qc_names.append(name)
            for cid, choice in enumerate(stmt['question']['choices']):
                ans = choice['text']
                ac = []
                ac_names = []
                for ent_obj in choice['text_ents']:
                    res = map_to_ddb(ent_obj)
                    for elm in res:
                        ddb_cid, name = elm
                        ac.append(ddb_cid)
                        ac_names.append(name)
                out = {'sent': sent, 'ans': ans, 'qc': qc, 'qc_names': qc_names, 'ac': ac, 'ac_names': ac_names}
                print (json.dumps(out), file=fout)

for fname in ["test"]:
    process_ddb(fname)


def load_ddb():
    with open('./data/ddb/ddb_names.json') as f:
        all_names = json.load(f)
    with open('./data/ddb/ddb_relas.json') as f:
        all_relas = json.load(f)
    relas_lst = []
    for key, val in all_relas.items():
        relas_lst.append(val)

    ddb_ptr_to_preferred_name = {}
    ddb_ptr_to_name = defaultdict(list)
    ddb_name_to_ptr = {}
    for key, val in all_names.items():
        item_name = key
        item_ptr = val[0]
        item_preferred = val[1]
        if item_preferred == "1":
            ddb_ptr_to_preferred_name[item_ptr] = item_name
        ddb_name_to_ptr[item_name] = item_ptr
        ddb_ptr_to_name[item_ptr].append(item_name)

    return (relas_lst, ddb_ptr_to_name, ddb_name_to_ptr, ddb_ptr_to_preferred_name)


relas_lst, ddb_ptr_to_name, ddb_name_to_ptr, ddb_ptr_to_preferred_name = load_ddb()


ddb_ptr_lst, ddb_names_lst = [], []
for key, val in ddb_ptr_to_preferred_name.items():
    ddb_ptr_lst.append(key)
    ddb_names_lst.append(val)

with open("./data/ddb/vocab.txt", "w") as fout:
    for ddb_name in ddb_names_lst:
        print (ddb_name, file=fout)

with open("./data/ddb/ptrs.txt", "w") as fout:
    for ddb_ptr in ddb_ptr_lst:
        print (ddb_ptr, file=fout)

id2concept = ddb_ptr_lst

merged_relations = [
    'belongs_to_the_category_of',
    'is_a_category',
    'may_cause',
    'is_a_subtype_of',
    'is_a_risk_factor_of',
    'is_associated_with',
    'may_contraindicate',
    'interacts_with',
    'belongs_to_the_drug_family_of',
    'belongs_to_drug_super-family',
    'is_a_vector_for',
    'may_be_allelic_with',
    'see_also',
    'is_an_ingradient_of',
    'may_treat'
]

relas_dict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "6": 5, "10": 6, "12": 7, "16": 8, "17": 9, "18": 10,
             "20": 11, "26": 12, "30": 13, "233": 14}

import networkx as nx

def construct_graph():
    concept2id = {w: i for i, w in enumerate(id2concept)}
    id2relation = merged_relations
    relation2id = {r: i for i, r in enumerate(id2relation)}
    graph = nx.MultiDiGraph()
    attrs = set()
    for relation in relas_lst:
        subj = concept2id[relation[0]]
        obj = concept2id[relation[1]]
        rel = relas_dict[relation[2]]
        weight = 1.
        graph.add_edge(subj, obj, rel=rel, weight=weight)
        attrs.add((subj, obj, rel))
        graph.add_edge(obj, subj, rel=rel + len(relation2id), weight=weight)
        attrs.add((obj, subj, rel + len(relation2id)))
    output_path = "./data/ddb/ddb.graph"
    nx.write_gpickle(graph, output_path)
    return concept2id, id2relation, relation2id, graph

concept2id, id2relation, relation2id, KG = construct_graph()

def load_kg():
    global cpnet, cpnet_simple
    cpnet = KG
    cpnet_simple = nx.Graph()
    for u, v, data in cpnet.edges(data=True):
        w = data['weight'] if 'weight' in data else 1.0
        if cpnet_simple.has_edge(u, v):
            cpnet_simple[u][v]['weight'] += w
        else:
            cpnet_simple.add_edge(u, v, weight=w)

load_kg()

from scipy.sparse import csr_matrix, coo_matrix
from multiprocessing import Pool

def concepts2adj(node_ids):
    global id2relation
    cids = np.array(node_ids, dtype=np.int32)
    n_rel = len(id2relation)
    n_node = cids.shape[0]
    adj = np.zeros((n_rel, n_node, n_node), dtype=np.uint8)
    for s in range(n_node):
        for t in range(n_node):
            s_c, t_c = cids[s], cids[t]
            if cpnet.has_edge(s_c, t_c):
                for e_attr in cpnet[s_c][t_c].values():
                    if e_attr['rel'] >= 0 and e_attr['rel'] < n_rel:
                        adj[e_attr['rel']][s][t] = 1
    adj = coo_matrix(adj.reshape(-1, n_node))
    return adj, cids

def concepts_to_adj_matrices_2hop_all_pair(data):
    qc_ids, ac_ids = data
    qa_nodes = set(qc_ids) | set(ac_ids)
    extra_nodes = set()
    for qid in qa_nodes:
        for aid in qa_nodes:
            if qid != aid and qid in cpnet_simple.nodes and aid in cpnet_simple.nodes:
                extra_nodes |= set(cpnet_simple[qid]) & set(cpnet_simple[aid])
    extra_nodes = extra_nodes - qa_nodes
    schema_graph = sorted(qc_ids) + sorted(ac_ids) + sorted(extra_nodes)
    arange = np.arange(len(schema_graph))
    qmask = arange < len(qc_ids)
    amask = (arange >= len(qc_ids)) & (arange < (len(qc_ids) + len(ac_ids)))
    adj, concepts = concepts2adj(schema_graph)
    return {'adj': adj, 'concepts': concepts, 'qmask': qmask, 'amask': amask, 'cid2score': None}

def generate_adj_data_from_grounded_concepts(grounded_path, cpnet_graph_path, cpnet_vocab_path, output_path, num_processes):
    global concept2id, id2concept, relation2id, id2relation, cpnet_simple, cpnet

    qa_data = []
    with open(grounded_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            dic = json.loads(line)
            q_ids = set(concept2id[c] for c in dic['qc'])
            if not q_ids:
                q_ids = {concept2id['31770']}
            a_ids = set(concept2id[c] for c in dic['ac'])
            if not a_ids:
                a_ids = {concept2id['325']}
            q_ids = q_ids - a_ids
            qa_data.append((q_ids, a_ids))

    with Pool(num_processes) as p:
        res = list(tqdm(p.imap(concepts_to_adj_matrices_2hop_all_pair, qa_data), total=len(qa_data)))

    lens = [len(e['concepts']) for e in res]
    print ('mean #nodes', int(np.mean(lens)), 'med', int(np.median(lens)), '5th', int(np.percentile(lens, 5)), '95th', int(np.percentile(lens, 95)))

    with open(output_path, 'wb') as fout:
        pickle.dump(res, fout)

    print(f'adj data saved to {output_path}')
    print()


for fname in ["test"]:
    grounded_path = f"./data/bioasq/grounded/{fname}.grounded.jsonl"
    kg_path       = f"./data/ddb/ddb.graph"
    kg_vocab_path = f"./data/ddb/ddb_ptrs.txt"
    output_path   = f"./data/bioasq/graph/{fname}.graph.adj.pk"

    generate_adj_data_from_grounded_concepts(grounded_path, kg_path, kg_vocab_path, output_path, 10)


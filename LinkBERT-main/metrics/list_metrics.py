import sys
import json

###########################################
# Takes three arguments:
# the path of predict_predictions.json
# the path of test.json
# the path to save all metrics as a json
###########################################

def load_labels(test_output_path, test_path):

    # load y_true
    y_true = []
    with open(test_path, "r") as f:
        for line in f:
            d = json.loads(line)
            y_true.append(d["answers"]["text"])
    y_true = [[s.lower() for s in inner_list] for inner_list in y_true]
    n = [len(inner_list) for inner_list in y_true]

    # load y_pred, list of lists
    with open(test_output_path, 'r') as f:
        test_outputs = json.load(f)

    y_pred = []
    ind = 0
    for i in test_outputs:
        preds = test_outputs[i]
        pred = []
        for j in range(len(preds)):
            if j == n[ind]: # the max length of golen set is 11
                break
            pred.append(preds[j]['text'].lower().strip())
        y_pred.append(pred)
        ind += 1

    return y_true, y_pred

def calculate_metrics(y_true, y_pred):
    TP = 0
    FP = 0
    FN = 0

    precisions = []
    recalls = []
    f1s = []

    for i in range(len(y_true)):
        golden = y_true[i]
        returned = y_pred[i]

        for entity in returned:
            if entity in golden:
                TP += 1
            else:
                FP += 1
        for entity in golden:
            if entity not in returned:
                FN += 1

        P = TP / (TP + FP)
        R = TP / (TP + FN)
        try:
            F1 = 2 * P * R / (P + R)
        except:
            F1 = 0
        precisions.append(P)
        recalls.append(R)
        f1s.append(F1)

    mean_p = sum(precisions)/len(precisions)
    mean_r = sum(recalls)/len(recalls)
    mean_f = sum(f1s)/len(f1s)
    
    return mean_p, mean_r, mean_f

def save_metrics(test_output_path, test_path,save_path):
    y_true, y_pred = load_labels(test_output_path, test_path)
    P, R, F1 = calculate_metrics(y_true, y_pred)

    print(f'**********\nMetrics for Factoid question:\n**********\nMean Precision: {P}\nRecall: {R}\nF-Measure: {F1}')

    metrics = {
        "Mean Precision": P,
        "Recall": R,
        "F-Measure": F1
    }
    with open(save_path, "w") as outfile:
        json.dump(metrics, outfile)

if __name__ == '__main__':
    
    test_output_path = sys.argv[1]
    test_path = sys.argv[2]
    save_path = sys.argv[3]
    save_metrics(test_output_path, test_path, save_path)

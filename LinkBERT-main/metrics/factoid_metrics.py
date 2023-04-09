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
            y_true.append(d["answers"]["text"][0].lower().strip())

    # load y_pred, list of lists
    with open(test_output_path, 'r') as f:
        test_outputs = json.load(f)

    y_pred = []
    for i in test_outputs:
        preds = test_outputs[i]
        pred = []
        for j in range(len(preds)):
            if j == 5:
                break
            pred.append(preds[j]['text'].lower().strip())
        y_pred.append(pred)

    return y_true, y_pred

def exact_acc(y_true, y_pred):
    correct = 0
    for i in range(len(y_pred)):
        if y_pred[i][0] == y_true[i]:
            correct += 1

    accuracy = correct / len(y_pred)
    return accuracy

def lenient_acc(y_true, y_pred):
    correct = 0
    for i in range(len(y_pred)):
        if y_true[i] in y_pred[i]:
            correct += 1

    accuracy = correct / len(y_pred)
    return accuracy

def MRR(y_true, y_pred):
    reciprocal_ranks = []
    for i in range(len(y_pred)):
        if y_true[i] in y_pred[i]:
            rank = y_pred[i].index(y_true[i]) + 1
            reciprocal_ranks.append(1.0 / rank)

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    return mrr

def save_metrics(test_output_path, test_path,save_path):
    y_true, y_pred = load_labels(test_output_path, test_path)
    e_acc = exact_acc(y_true, y_pred)
    l_acc = lenient_acc(y_true, y_pred)
    mrr = MRR(y_true, y_pred)

    print(f'**********\nMetrics for Factoid question:\n**********\nExact Accuracy: {e_acc}\nLenient Accuracy: {l_acc}\nMRR: {mrr}')

    metrics = {
        "Exact Accuracy": e_acc,
        "Lenient Accuracy": l_acc,
        "MRR": mrr
    }
    with open(save_path, "w") as outfile:
        json.dump(metrics, outfile)

if __name__ == '__main__':
    
    test_output_path = sys.argv[1]
    test_path = sys.argv[2]
    save_path = sys.argv[3]
    save_metrics(test_output_path, test_path, save_path)

import sys
import json
from sklearn import metrics

###########################################
# Takes two arguments:
# the path of test_output.json
# the path to save all metrics as a json
###########################################

def load_labels(test_output_path):

    with open(test_output_path, "r") as f:
        test_output = json.load(f)
           
    y_pred = test_output['predictions']
    y_true = test_output['label_ids']

    y_pred = [lst.index(max(lst)) for lst in y_pred]

    return y_true, y_pred

def calculate_accuracy(y_true, y_pred):
    
    return metrics.accuracy_score(y_true, y_pred)

def f1_no(y_true, y_pred):

    return metrics.f1_score(y_true, y_pred, pos_label=0)

def f1_yes(y_true, y_pred):

    return metrics.f1_score(y_true, y_pred, pos_label=1)

def f1_macro(y_true, y_pred):

    return metrics.f1_score(y_true, y_pred, average='macro')

def save_metrics(test_output_path, save_path):

    y_true, y_pred = load_labels(test_output_path)
    acc = calculate_accuracy(y_true, y_pred)
    f1_no_met = f1_no(y_true, y_pred)
    f1_yes_met = f1_yes(y_true, y_pred)
    f1_macro_met = f1_macro(y_true, y_pred)

    print(f'**********\nMetrics for Yes/No question:\n**********\nAccuracy: {acc}\nF1_No: {f1_no_met}\nF1_Yes: {f1_yes_met}\nF1_Macro: {f1_macro_met}')

    metrics = {
        "Accuracy": acc,
        "F1_No": f1_no_met,
        "F1_Yes": f1_yes_met,
        "F1_Macro": f1_macro_met
    }
    with open(save_path, "w") as outfile:
        json.dump(metrics, outfile)


if __name__ == '__main__':
    
    test_output_path = sys.argv[1]
    save_path = sys.argv[2]
    save_metrics(test_output_path, save_path)

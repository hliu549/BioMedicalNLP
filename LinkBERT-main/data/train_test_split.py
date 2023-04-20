import json
from sklearn.model_selection import train_test_split
import sys
import os

def spliting(data):

    train_data, test_data = train_test_split(data, test_size=0.2, random_state=1)
    test_data, val_data = train_test_split(test_data, test_size=0.5, random_state=1)
    return train_data, test_data, val_data

def load_data(data_path):

    with open(data_path, 'r') as f:
        data = json.load(f)
    return data['data']['paragraphs']

def save_data(data, save_path):
    with open(save_path, 'w') as f:
        for item in data:
            json.dump(item, f)
            f.write('\n')


if __name__ == '__main__':
    
    input_file = sys.argv[1]
    output_path = sys.argv[2]

    data = load_data(input_file)
    train_data, test_data, val_data = spliting(data)

    save_data(train_data, os.path.join(output_path, 'train.json'))
    save_data(test_data, os.path.join(output_path, 'test.json'))
    save_data(val_data, os.path.join(output_path, 'dev.json'))

'''
# Preparing train data
lable must int or use map change text to int
lable start 0
train_data = [
    ["Aragorn was the heir of Isildur", 1],
    ["Frodo was the heir of Isildur", 0],
    ["Pippin is stronger than Merry", 2],
]
train_df = pd.DataFrame(train_data)
train_df.columns = ["text", "labels"]

# Preparing eval data
'''
import json
import traceback
from sklearn.model_selection import KFold
from config import CUR_PATH
import pandas as pd
from utils.srf_log import logger


def loan_usage_example():
    with open(f'{CUR_PATH}/data/loan_usage/loan_usage.txt') as f:
        index = 0
        label_map = {}
        data = []
        for line in f.readlines():
            if line.startswith('#') or not line.strip():
                continue
            else:
                label, texts = line.split(' ## ')
                label_map[index] = label.strip()
                for text in texts.strip().split(','):
                    data.append([text, index])
                index += 1
        df = pd.DataFrame(data)
        df.columns = ["text", "labels"]
    with open(f'{CUR_PATH}/data/loan_usage/label_map.json','w') as f1:
        json.dump(label_map,f1)
    return df

def split_example_KFold(df):
    '''
    划分验证集与训练集
    :param df:
    :return:
    '''
    try:
        kf = KFold(shuffle=True, random_state=2)
        res = next(kf.split(df), None)
        train = df.iloc[res[0]]
        dev = df.iloc[res[1]]
        return train,dev
    except Exception:
        logger.error(f'_splite_example is error:\n{traceback.format_exc()}')


def get_label_map():
    with open(f'{CUR_PATH}/data/loan_usage/label_map.json') as f:
        label_map = json.load(f)
        return label_map

if __name__ == '__main__':
    r = loan_usage_example()
    r1,r2 =split_example_KFold(r)
    print(r2)
    print(r1)

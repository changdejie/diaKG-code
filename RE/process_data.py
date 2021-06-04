# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 下午2:08
# @Author  : liuliping
# @File    : process_data.py.py
# @description: 从原始数据抽取实体-关系

import json
import os
import glob
import copy
import random

total_count = {}

def custom_RE(file_path, output_path):
    #
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line.strip()) for line in f.readlines()]

    result = []
    relation_count = {}
    for sub in data: # 行
        ner_relation = {}
        relation_set = set()
        ner_data = sub['sd_result']['items']
        text = sub['text']
        segments = [i for i in range(len(text)) if text[i] in {'。', '？', '！', '；', '：', '，'}]
        for ner in ner_data:
            ner_text = ner['meta']['text']
            start, end = ner['meta']['segment_range']
            ner_label = ner['labels']['Entity']
            relations = ner['labels'].get('Relation', [])
            for rel in relations:
                relation_set.add(rel)

            ner_relation[f'{ner_text}#{ner_label}#{start}#{end}'] = relations

        for rel in relation_set:
            tmp = []
            for ner, rels in ner_relation.items():

                if rel in rels and (len(tmp) == 0 or tmp[0].split('#')[1] != ner.split('#')[1]):
                    tmp.append(ner)

                if len(tmp) == 2:
                    ner_1 = tmp[0].split('#')
                    ner_2 = tmp[1].split('#')

                    index = [int(d) for d in ner_1[2:]] + [int(d) for d in ner_2[2:]]

                    min_idx, max_idx = min(index), max(index)

                    sub_text = text[:segments[0]] if segments and segments[0] >= max_idx else text[:]

                    min_seg = 0
                    max_seg = len(text)
                    for i in range(len(segments) - 1):
                        if segments[i] <= min_idx <= segments[i + 1]:
                            min_seg = segments[i]
                            break
                    for i in range(len(segments) - 1):
                        if segments[i] <= max_idx <= segments[i + 1]:
                            max_seg = segments[i + 1]
                            break

                    if min_seg != 0 or max_seg != len(text):
                        sub_text = text[min_seg + 1: max_seg]
                    rel = rel.split('-'[0])[0].strip().replace('?', '')
                    result.append([t.split('#')[0] for t in tmp] + [rel, sub_text])
                    relation_count[rel] = relation_count.setdefault(rel, 0) + 1
                    total_count[rel] = total_count.setdefault(rel, 0) + 1
                    break

    with open(os.path.join(output_path, 'custom_RE_{}.txt'.format(os.path.split(file_path)[1].split('.')[0])),
            'w', encoding='utf-8') as fw:
        fw.write('\n'.join(['\t'.join(t) for t in result]))

    print(os.path.basename(file_path), relation_count)


if __name__ == '__main__':
    input_path = '../data/糖尿病标注数据4.28/' # 原始数据path
    output_path = 'data/custom_RE'
    os.makedirs('data/custom_RE/', exist_ok=True)

    files = glob.glob(f'{input_path}/*.txt')
    for fil in files:
        custom_RE(fil, output_path)
    print('total', total_count)

    relations = {}
    files = glob.glob(f'{output_path}/*.txt')
    for fil in files:
        with open(fil, 'r', encoding='utf-8') as f:
            data = f.readlines()
        for sub in data:
            l = sub.strip().split('\t')
            relations.setdefault(l[2], []).append(sub)
    # 拆分数据集 train:dev:test=6:2:2
    train_data, dev_data, test_data = [], [], []
    for rel, val in relations.items():
        print(rel, len(val))
        length = len(val)
        random.shuffle(val)
        train_data.extend(val[:length // 10 * 6])
        dev_data.extend(val[length // 10 * 6: length // 10 * 8])
        test_data.extend(val[length // 10 * 8:])

    with open('data/train.txt', 'w', encoding='utf-8') as fw:
        random.shuffle(train_data)
        fw.write(''.join(train_data))

    with open('data/dev.txt', 'w', encoding='utf-8') as fw:
        random.shuffle(dev_data)
        fw.write(''.join(dev_data))

    with open('data/test.txt', 'w', encoding='utf-8') as fw:
        random.shuffle(test_data)
        fw.write(''.join(test_data))

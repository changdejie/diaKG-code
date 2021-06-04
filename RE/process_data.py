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

# 12.txt {'Rel_Anatomy_Disease': 20, 'Rel_Test_items_Disease': 30, 'Rel_Drug_Disease': 81, 'Rel_SideEff_Disease': 2, 'Rel_Type_Disease': 27, 'Rel_SideEff_Drug': 77, 'Rel_Treatment_Disease': 16, 'Rel_Pathogenesis_Disease': 5, 'Rel_Amount_Drug': 20, 'Rel_Method_Drug': 7, 'Rel_Frequency_Drug': 3, 'Rel_Test_Disease': 1, 'Rel_Operation_Disese': 1}
# 38.txt {'Rel_Anatomy_Disease': 7, 'Rel_Pathogenesis_Disease': 2, 'Rel_Type_Disease': 2, 'Rel_Test_items_Disease': 13, 'Rel_Reason_Disease': 7, 'Rel_Operation_Disese': 1, 'Rel_Drug_Disease': 8, 'Rel_SideEff_Drug': 1}
# 39.txt {'Rel_Anatomy_Disease': 19, 'Rel_Pathogenesis_Disease': 2, 'Rel_Symptom_Disease': 11, 'Rel_Test_items_Disease': 41, 'Rel_Type_Disease': 7, 'Rel_Treatment_Disease': 14, 'Rel_Drug_Disease': 34, 'Rel_SideEff_Drug': 23, 'Rel_Method_Drug': 5, 'Rel_Frequency_Drug': 6, 'Rel_Amount_Drug': 4, 'Rel_SideEff_Disease': 3}
# 28.txt {'Rel_Test_items_Disease': 37, 'Rel_Pathogenesis_Disease': 2, 'Rel_SideEff_Drug': 5, 'Rel_Reason_Disease': 6, 'Rel_Symptom_Disease': 2, 'Rel_Anatomy_Disease': 6, 'Rel_Test_Disease': 2, 'Rel_Type_Disease': 2, 'Rel_Drug_Disease': 2}
# 7.txt {'Rel_Anatomy_Disease': 40, 'Rel_Type_Disease': 20, 'Rel_Test_items_Disease': 62, 'Rel_Reason_Disease': 5, 'Rel_Test_Disease': 8, 'Rel_Method_Drug': 4, 'Rel_Symptom_Disease': 6, 'Rel_Pathogenesis_Disease': 1, 'Rel_Amount_Drug': 2, 'Rel_SideEff_Drug': 13, 'Rel_Drug_Disease': 10}
# 34.txt {'Rel_Type_Disease': 34, 'Rel_Pathogenesis_Disease': 8, 'Rel_Symptom_Disease': 15, 'Rel_Test_items_Disease': 39, 'Rel_Anatomy_Disease': 10, 'Rel_Treatment_Disease': 10, 'Rel_Drug_Disease': 7, 'Rel_SideEff_Drug': 8, 'Rel_Frequency_Drug': 3, 'Rel_Amount_Drug': 6, 'Rel_Operation_Disese': 1, 'Rel_Test_Disease': 1, 'Rel_Method_Drug': 2}
# 17.txt {'Rel_Test_items_Disease': 64, 'Rel_Drug_Disease': 14, 'Rel_Type_Disease': 5, 'Rel_Anatomy_Disease': 21, 'Rel_Operation_Disese': 2, 'Rel_Symptom_Disease': 2, 'Rel_Frequency_Drug': 12, 'Rel_Amount_Drug': 10, 'Rel_Method_Drug': 54, 'Rel_Pathogenesis_Disease': 1, 'Rel_Treatment_Disease': 8, 'Rel_SideEff_Drug': 5, 'Rel_Reason_Disease': 9, 'Rel_Test_Disease': 1}
# 15.txt {'Rel_Anatomy_Disease': 92, 'Rel_Type_Disease': 63, 'Rel_Test_items_Disease': 37, 'Rel_Test_Disease': 11, 'Rel_Treatment_Disease': 6, 'Rel_Reason_Disease': 10, 'Rel_Drug_Disease': 87, 'Rel_SideEff_Drug': 18, 'Rel_Amount_Drug': 1, 'Rel_Duration_Drug': 4, 'Rel_Pathogenesis_Disease': 3, 'Rel_Operation_Disese': 1}
# 32.txt {'Rel_Anatomy_Disease': 12, 'Rel_Type_Disease': 4, 'Rel_Test_items_Disease': 10, 'Rel_Treatment_Disease': 3, 'Rel_Frequency_Drug': 2, 'Rel_SideEff_Drug': 7, 'Rel_Amount_Drug': 4, 'Rel_Method_Drug': 1, 'Rel_Drug_Disease': 24, 'Rel_Duration_Drug': 1, 'Rel_Symptom_Disease': 2}
# 29.txt {'Rel_Symptom_Disease': 63, 'Rel_Test_items_Disease': 10, 'Rel_Anatomy_Disease': 29, 'Rel_Type_Disease': 9, 'Rel_Operation_Disese': 2, 'Rel_Pathogenesis_Disease': 3, 'Rel_Drug_Disease': 32, 'Rel_Duration_Drug': 2, 'Rel_Method_Drug': 7, 'Rel_Treatment_Disease': 1, 'Rel_Test_Disease': 2}
# 40.txt {'Rel_Treatment_Disease': 53, 'Rel_Reason_Disease': 24, 'Rel_Symptom_Disease': 6, 'Rel_Test_items_Disease': 35, 'Rel_Pathogenesis_Disease': 1, 'Rel_Anatomy_Disease': 7, 'Rel_Drug_Disease': 2, 'Rel_Type_Disease': 4}
# 9.txt {'Rel_Type_Disease': 111, 'Rel_Anatomy_Disease': 83, 'Rel_Reason_Disease': 4, 'Rel_Test_items_Disease': 29, 'Rel_Pathogenesis_Disease': 2, 'Rel_Drug_Disease': 46, 'Rel_SideEff_Drug': 14, 'Rel_Test_Disease': 7, 'Rel_Amount_Drug': 6, 'Rel_Method_Drug': 1, 'Rel_Frequency_Drug': 4, 'Rel_Treatment_Disease': 5}
# 41.txt {'Rel_Test_items_Disease': 31, 'Rel_Anatomy_Disease': 86, 'Rel_Symptom_Disease': 49, 'Rel_Type_Disease': 23, 'Rel_Treatment_Disease': 25, 'Rel_Reason_Disease': 21, 'Rel_SideEff_Drug': 19, 'Rel_Amount_Drug': 14, 'Rel_Duration_Drug': 2, 'Rel_SideEff_Disease': 4, 'Rel_Drug_Disease': 20, 'Rel_Method_Drug': 7, 'Rel_Frequency_Drug': 1, 'Rel_Test_Disease': 6, 'Rel_Operation_Disese': 4, 'Rel_Pathogenesis_Disease': 1}
# 11.txt {'Rel_Drug_Disease': 40, 'Rel_Method_Drug': 4, 'Rel_Test_items_Disease': 7, 'Rel_Type_Disease': 23, 'Rel_Frequency_Drug': 1, 'Rel_SideEff_Drug': 55, 'Rel_Anatomy_Disease': 22, 'Rel_Reason_Disease': 1, 'Rel_Treatment_Disease': 1, 'Rel_Amount_Drug': 3, 'Rel_Test_Disease': 1}
# 24.txt {'Rel_Type_Disease': 22, 'Rel_Anatomy_Disease': 18, 'Rel_Test_items_Disease': 59, 'Rel_Symptom_Disease': 5, 'Rel_Pathogenesis_Disease': 2, 'Rel_Drug_Disease': 26, 'Rel_Reason_Disease': 1, 'Rel_Treatment_Disease': 1, 'Rel_Frequency_Drug': 1, 'Rel_Method_Drug': 4, 'Rel_SideEff_Drug': 10, 'Rel_Duration_Drug': 1, 'Rel_SideEff_Disease': 4}
# 25.txt {'Rel_Anatomy_Disease': 49, 'Rel_Type_Disease': 18, 'Rel_Test_Disease': 3, 'Rel_Reason_Disease': 9, 'Rel_Symptom_Disease': 7, 'Rel_SideEff_Drug': 26, 'Rel_Frequency_Drug': 1, 'Rel_Amount_Drug': 4, 'Rel_Test_items_Disease': 9, 'Rel_Drug_Disease': 27, 'Rel_Method_Drug': 4, 'Rel_SideEff_Disease': 8}
# 5.txt {'Rel_Operation_Disese': 1, 'Rel_Type_Disease': 4, 'Rel_Test_items_Disease': 1}
# 2.txt {'Rel_Test_items_Disease': 62, 'Rel_Type_Disease': 14, 'Rel_Anatomy_Disease': 10, 'Rel_Test_Disease': 2, 'Rel_Reason_Disease': 9, 'Rel_SideEff_Drug': 2, 'Rel_Pathogenesis_Disease': 1, 'Rel_Drug_Disease': 2, 'Rel_Treatment_Disease': 1}
# 16.txt {'Rel_Drug_Disease': 102, 'Rel_Type_Disease': 35, 'Rel_Test_items_Disease': 31, 'Rel_Amount_Drug': 23, 'Rel_SideEff_Drug': 64, 'Rel_Anatomy_Disease': 17, 'Rel_Frequency_Drug': 2, 'Rel_Treatment_Disease': 6, 'Rel_Method_Drug': 7, 'Rel_Duration_Drug': 6, 'Rel_Pathogenesis_Disease': 4, 'Rel_Test_Disease': 7, 'Rel_Operation_Disese': 1, 'Rel_Symptom_Disease': 1}
# 36.txt {'Rel_Anatomy_Disease': 37, 'Rel_Test_items_Disease': 21, 'Rel_Type_Disease': 10, 'Rel_Reason_Disease': 3, 'Rel_Symptom_Disease': 6, 'Rel_Test_Disease': 20, 'Rel_Drug_Disease': 24, 'Rel_SideEff_Drug': 1, 'Rel_Treatment_Disease': 12}
# 6.txt {'Rel_Anatomy_Disease': 81, 'Rel_Operation_Disese': 3, 'Rel_Symptom_Disease': 1, 'Rel_Treatment_Disease': 33, 'Rel_Type_Disease': 41, 'Rel_Test_items_Disease': 87, 'Rel_Reason_Disease': 4, 'Rel_Pathogenesis_Disease': 22, 'Rel_Test_Disease': 37, 'Rel_Duration_Drug': 3, 'Rel_Drug_Disease': 120, 'Rel_SideEff_Disease': 2, 'Rel_SideEff_Drug': 24, 'Rel_Amount_Drug': 5, 'Rel_Frequency_Drug': 1, 'Rel_Method_Drug': 1}
# 19.txt {'Rel_Drug_Disease': 16, 'Rel_Type_Disease': 10, 'Rel_Symptom_Disease': 4, 'Rel_SideEff_Drug': 12, 'Rel_Amount_Drug': 6, 'Rel_Method_Drug': 3, 'Rel_Test_items_Disease': 4, 'Rel_Treatment_Disease': 5, 'Rel_SideEff_Disease': 2, 'Rel_Anatomy_Disease': 2}
# 27.txt {'Rel_Drug_Disease': 20, 'Rel_Type_Disease': 9, 'Rel_Test_items_Disease': 37, 'Rel_SideEff_Drug': 12, 'Rel_Pathogenesis_Disease': 2, 'Rel_Method_Drug': 7, 'Rel_Frequency_Drug': 6, 'Rel_Reason_Disease': 1, 'Rel_SideEff_Disease': 6, 'Rel_Amount_Drug': 14, 'Rel_Duration_Drug': 2, 'Rel_Symptom_Disease': 2, 'Rel_Treatment_Disease': 2}
# 3.txt {'Rel_Drug_Disease': 27, 'Rel_Type_Disease': 14, 'Rel_Test_items_Disease': 12, 'Rel_Pathogenesis_Disease': 5, 'Rel_Anatomy_Disease': 8, 'Rel_Frequency_Drug': 8, 'Rel_Method_Drug': 5, 'Rel_SideEff_Disease': 10, 'Rel_SideEff_Drug': 1}
# 33.txt {'Rel_Drug_Disease': 33, 'Rel_Type_Disease': 24, 'Rel_Test_items_Disease': 19, 'Rel_Frequency_Drug': 22, 'Rel_SideEff_Drug': 24, 'Rel_Method_Drug': 18, 'Rel_Amount_Drug': 23, 'Rel_Pathogenesis_Disease': 6, 'Rel_Anatomy_Disease': 6, 'Rel_Treatment_Disease': 3, 'Rel_SideEff_Disease': 3, 'Rel_Duration_Drug': 1}
# 26.txt {'Rel_Type_Disease': 28, 'Rel_Drug_Disease': 25, 'Rel_Anatomy_Disease': 10, 'Rel_Method_Drug': 2, 'Rel_Duration_Drug': 3, 'Rel_Test_Disease': 1, 'Rel_SideEff_Drug': 9, 'Rel_Test_items_Disease': 18, 'Rel_Amount_Drug': 4, 'Rel_Frequency_Drug': 1}
# 20.txt {'Rel_Type_Disease': 6, 'Rel_Method_Drug': 5, 'Rel_Test_items_Disease': 4, 'Rel_Anatomy_Disease': 2, 'Rel_Treatment_Disease': 10, 'Rel_Symptom_Disease': 6, 'Rel_Drug_Disease': 3}
# 35.txt {'Rel_Drug_Disease': 22, 'Rel_Type_Disease': 9, 'Rel_Method_Drug': 2, 'Rel_SideEff_Drug': 22, 'Rel_Anatomy_Disease': 4, 'Rel_SideEff_Disease': 1, 'Rel_Test_items_Disease': 1}
# 31.txt {'Rel_Treatment_Disease': 5, 'Rel_Test_items_Disease': 1}
# 8.txt {'Rel_Test_items_Disease': 13, 'Rel_Method_Drug': 3, 'Rel_SideEff_Drug': 14, 'Rel_Type_Disease': 27, 'Rel_Drug_Disease': 49, 'Rel_Treatment_Disease': 9, 'Rel_Pathogenesis_Disease': 3, 'Rel_Anatomy_Disease': 8, 'Rel_SideEff_Disease': 1}
# 13.txt {'Rel_Test_Disease': 60, 'Rel_Type_Disease': 55, 'Rel_Anatomy_Disease': 32, 'Rel_Drug_Disease': 104, 'Rel_SideEff_Drug': 28, 'Rel_Test_items_Disease': 67, 'Rel_Pathogenesis_Disease': 7, 'Rel_Reason_Disease': 5, 'Rel_Treatment_Disease': 14, 'Rel_Amount_Drug': 2, 'Rel_Duration_Drug': 3}
# 23.txt {'Rel_Drug_Disease': 5, 'Rel_Test_items_Disease': 5, 'Rel_Pathogenesis_Disease': 2, 'Rel_Type_Disease': 4, 'Rel_Frequency_Drug': 21, 'Rel_Treatment_Disease': 1, 'Rel_Method_Drug': 7, 'Rel_Amount_Drug': 7, 'Rel_SideEff_Drug': 12, 'Rel_Anatomy_Disease': 1}
# 4.txt {'Rel_Anatomy_Disease': 7, 'Rel_Type_Disease': 41, 'Rel_Reason_Disease': 2, 'Rel_Test_items_Disease': 31, 'Rel_Pathogenesis_Disease': 2, 'Rel_Drug_Disease': 30, 'Rel_SideEff_Drug': 16, 'Rel_Amount_Drug': 3, 'Rel_Method_Drug': 1, 'Rel_Frequency_Drug': 2, 'Rel_Treatment_Disease': 5}
# 18.txt {'Rel_Test_items_Disease': 16, 'Rel_Drug_Disease': 31, 'Rel_Type_Disease': 20, 'Rel_Amount_Drug': 8, 'Rel_Anatomy_Disease': 24, 'Rel_Frequency_Drug': 9, 'Rel_Test_Disease': 1, 'Rel_Symptom_Disease': 12, 'Rel_SideEff_Drug': 13, 'Rel_SideEff_Disease': 7, 'Rel_Method_Drug': 5, 'Rel_Treatment_Disease': 5}
# 10.txt {'Rel_Anatomy_Disease': 59, 'Rel_Test_Disease': 22, 'Rel_Symptom_Disease': 36, 'Rel_Test_items_Disease': 3, 'Rel_Type_Disease': 7, 'Rel_Pathogenesis_Disease': 2, 'Rel_Drug_Disease': 7, 'Rel_Treatment_Disease': 7}
# 1.txt {'Rel_Drug_Disease': 31, 'Rel_Type_Disease': 20, 'Rel_Test_items_Disease': 11, 'Rel_Pathogenesis_Disease': 12, 'Rel_Anatomy_Disease': 13, 'Rel_SideEff_Drug': 21, 'Rel_Duration_Drug': 1, 'Rel_Frequency_Drug': 1}
# 37.txt {'Rel_Anatomy_Disease': 62, 'Rel_Reason_Disease': 7, 'Rel_Symptom_Disease': 40, 'Rel_Operation_Disese': 2, 'Rel_Test_items_Disease': 5, 'Rel_SideEff_Disease': 6, 'Rel_SideEff_Drug': 11, 'Rel_Drug_Disease': 12, 'Rel_Type_Disease': 2, 'Rel_Amount_Drug': 5, 'Rel_Frequency_Drug': 3, 'Rel_Duration_Drug': 2, 'Rel_Method_Drug': 3}
# 22.txt {'Rel_Drug_Disease': 32, 'Rel_Type_Disease': 24, 'Rel_Test_items_Disease': 6, 'Rel_Anatomy_Disease': 6}
# 14.txt {'Rel_Test_items_Disease': 42, 'Rel_Reason_Disease': 8, 'Rel_Type_Disease': 5, 'Rel_SideEff_Disease': 6, 'Rel_Treatment_Disease': 2, 'Rel_Operation_Disese': 1, 'Rel_Test_Disease': 4, 'Rel_Anatomy_Disease': 6, 'Rel_Drug_Disease': 7, 'Rel_Method_Drug': 22, 'Rel_SideEff_Drug': 6, 'Rel_Duration_Drug': 8, 'Rel_Amount_Drug': 5, 'Rel_Symptom_Disease': 2, 'Rel_Frequency_Drug': 1, 'Rel_Pathogenesis_Disease': 1}
# 21.txt {'Rel_Type_Disease': 33, 'Rel_Test_items_Disease': 16, 'Rel_Reason_Disease': 6, 'Rel_Pathogenesis_Disease': 3, 'Rel_Symptom_Disease': 4, 'Rel_Anatomy_Disease': 5, 'Rel_Treatment_Disease': 5, 'Rel_Drug_Disease': 5, 'Rel_SideEff_Drug': 7, 'Rel_Amount_Drug': 3, 'Rel_Operation_Disese': 1}
# 30.txt {'Rel_Drug_Disease': 41, 'Rel_Anatomy_Disease': 7, 'Rel_Type_Disease': 23, 'Rel_Method_Drug': 6, 'Rel_Test_items_Disease': 9, 'Rel_SideEff_Disease': 3, 'Rel_SideEff_Drug': 30, 'Rel_Treatment_Disease': 1, 'Rel_Duration_Drug': 12, 'Rel_Amount_Drug': 7}
# {'Rel_Anatomy_Disease': 928, 'Rel_Test_items_Disease': 1035, 'Rel_Drug_Disease': 1208, 'Rel_SideEff_Disease': 68, 'Rel_Type_Disease': 839, 'Rel_SideEff_Drug': 610, 'Rel_Treatment_Disease': 269, 'Rel_Pathogenesis_Disease': 105, 'Rel_Amount_Drug': 189, 'Rel_Method_Drug': 197, 'Rel_Frequency_Drug': 111, 'Rel_Test_Disease': 197, 'Rel_Operation_Disese': 21, 'Rel_Reason_Disease': 142, 'Rel_Symptom_Disease': 282, 'Rel_Duration_Drug': 51}


# DiaKG: an Annotated Diabetes Dataset for Medical Knowledge Graph Construction

This is the source code of the DiaKG [paper](https://arxiv.org/abs/2105.15033).

## DataSet 

### Overview
The DiaKG dataset is derived from 41 diabetes guidelines and consensus, which are from authoritative Chinese journals including basic research, clinical research, drug usage, clinical cases, diagnosis and treatment methods, etc. The dataset covers the most extensive field of research content and hotspot in recent years. The annotation process is done by 2 seasoned endocrinologists and 6 M.D. candidates, and finally conduct a high-quality diabates database which contains 22,050 entities and 6,890 relations in total.

### Get the Data
The codebase only provides some sample annotation files. If you want to download the fullset, please apply at [Tianchi Platform](https://tianchi.aliyun.com/dataset/dataDetail?dataId=88836).

### Data Format
The dataset is exhibited as a hierachical structure with "document-paragraph-sentence" information. All the entities and sentences are labelled on the sentence level. Below is an example:

```
{ 
  "doc_id": "1", // string, document id 
  "paragraphs": [ // array, paragraphs 
    {
      "paragraph_id": "0", // string, paragraph id
      "paragraph": "中国成人2型糖尿病胰岛素促泌剂应用的专家共识", // string, paragraph text
      "sentences": [ // array, sentences
        {
          "sentence_id": "0", // string, sentence id
          "sentence": "中国成人2型糖尿病胰岛素促泌剂应用的专家共识", // string, sentence text
          "start_idx": 0, // int, sentence start index in the current paragraph
          "end_idx": 22, // int, sentence end index in the current paragraph
          "entities": [ // array, entities in the current sentence
            {
              "entity_id": "T0", // string, entity id
              "entity": "2型糖尿病", // string, entity text
              "entity_type": "Disease", // string, entity type
              "start_idx": 4, // int, entity start index in the sentence
              "end_idx": 9 // int, entity end index in the sentence
            },
            {
              "entity_id": "T1",
              "entity": "2型",
              "entity_type": "Class",
              "start_idx": 4,
              "end_idx": 6
            },
            {
              "entity_id": "T2",
              "entity": "胰岛素促泌剂",
              "entity_type": "Drug",
              "start_idx": 9,
              "end_idx": 15
            }
          ],
          "relations": [ // array, relations in the current sentence
            {
              "relation_type": "Drug_Disease", // string, relation type
              "relation_id": "R0", // string, relation id
              "head_entity_id": "T2", // string, head entity id
              "tail_entity_id": "T0" // string, tail entity id
            },
            {
              "relation_type": "Class_Disease",
              "relation_id": "R1",
              "head_entity_id": "T1",
              "tail_entity_id": "T0"
            }
          ]
        }
      ]
    },
    {
      "paragraph_id": "1", // string, paragraph id
      "paragraph": "xxx" // string, paragraph text
      "sentences": [
        ...
      ] 
    },
    ...
  ] 
}
```

### Data Statistic

#### Entity


|Entity | Freq | Fraction(%) | Avg Length  |Entity | Freq | Fraction(%) | Avg Length |
|-----|--------|--------|---------|-------|-----------|----------|----------|
|Disease        |5743 |26.05% |7.27 |Frequency      |156  |0.71%  |4.71
|Class          |1262 |5.72%  |4.27 |Method         |399  |1.81%  |6.09
|Reason         |175  |0.79%  |7.34 |Treatment      |756  |3.43%  |7.97
|Pathogenesis   |202  |0.92%  |10.27|Operation      |133  |0.60%  |9.02
|Symptom        |479  |2.17%  |5.82 |ADE            |874  |3.96%  |5.06
|Test           |489  |2.22%  |6.1  |Anatomy        |1876 |8.51%  |3.1
|Test_items     |2718 |12.33% |7.65 |Level          |280  |1.27%  |2.93
|Test_Value     |1356 |6.15%  |9.49 |Duration       |69   |0.31%  |3.68
|Drug           |4782 |21.69% |7.79 |Amount         |301  |1.37%  |6.74
|Total          |22050|100%   |6.5


#### Relation

|Relation|Freq |Fraction(%)|Avg Cross-sentence Number |Relation|Freq |Fraction(%)|Avg Cross-sentence Number | 
|-----------|------|-------|---------|--------|----------|------|-------|
|Test_items_Disease  |1171  |17%　  |2.3  |Type_Disease         |854   |12.39% |2.13 |
|Anatomy_Disease     |1072  |15.56% |2.07 |Reason_Disease       |164   |2.38%  |2.42 |
|Drug_Disease        |1315  |19.09% |2.5  |Duration_Drug        |61    |0.89%  |2.79 |
|Method_Drug         |185   |2.69%  |2.41 　|Symptom_Disease    |283   |4.11%  |2.08 |
|Treatment_Disease   |354   |5.14%  |2.6   |Amount_Drug         |195   |2.83%  |2.62 |
|Pathogenesis_Disease|130   |1.89%  |1.97  |SideEff_Drug        |693   |10.06% |2.65 |
|Test_Disease        |271   |3.93%  |2.27  |Frequency_Drug      |103   |1.49%  |1.97 |
|Operation_Disese    |37    |0.54%  |2.57  
|Total               |6890  |100% |2.33 |


* Note: **Avg Cross-sentence Number** means the average sentences that the two entities that compose a relation locate, since the annotation is conducted on document level and cross-sentence relation is allowed.
 
## Experiments

### NER

We use [MRC-BERT](https://github.com/changdejie/diaKG-code/tree/mrcforner) as our baseline model, and the source code is in the **NER** directory.

#### How to run
```
cd NER

## Training:
python trainer.py --data_dir entity_type_data --bert_config models/chinese_roberta_wwm_large_ext_pytorch --batch_size 16 --max_epochs 10 --gpus 1

## Inference:
python evaluate.py 

```

#### Results

|Entity       |precision|recall   |F1     |Entity       |precision|recall   |F1     |
|-------------|---------|---------|-------|-------------|---------|---------|-------|
|Frequency    |1.0      |0.9      |0.947  |ADE          | 0.791   | 0.815   | 0.803 |
|Method       | 0.895   | 0.927   | 0.911 |Duration     | 0.833   | 0.714   | 0.769 |
|Class        | 0.852   | 0.949   | 0.898 |Amount       | 0.73    | 0.75    | 0.74  |
|Drug         | 0.881   | 0.902   | 0.892 |Operation    | 0.75    | 0.714   | 0.732 |
|Level        | 0.841   | 0.902   | 0.871 |Treatment    | 0.679   | 0.783   | 0.727 |
|Anatomy      | 0.834   | 0.869   | 0.851 |Test         | 0.855   | 0.609   | 0.711 |
|Disease      | 0.794   | 0.91    | 0.848 |Pathogenesis | 0.595   | 0.667   | 0.629 |
|Test\_Items  | 0.823   | 0.815   | 0.818 |Symptom      | 0.535   | 0.535   | 0.535 |
|Test\_Value  | 0.828   | 0.787   | 0.807 |Reason       | 0.333   | 0.3     | 0.316 |
|total        |0.814    |0.853    |0.833  |


### RE

We use [Bi-directional GRU-Attention](https://github.com/crownpku/Information-Extraction-Chinese) as our baseline model, and the source code is in the **RE** directory.

#### How to run

Details in folder RE/README.md


#### Results
|Relation   |precision  |recall |F1     |Relation   |precision  |recall |F1     |
|-------------|---------|---------|-------|-------------|---------|---------|-------|
Class\_Disease        | 0.968 | 0.874 | 0.918 |Duration\_Drug        | 0.833 | 0.769 | 0.8   |
ADE\_Drug             | 0.892 | 0.892 | 0.892 |Frequency\_Drug       | 0.750 | 0.783 | 0.766 |
Drug\_Disease         | 0.864 | 0.913 | 0.888 |Symptom\_Disease      | 0.689 | 0.712 | 0.7   |
Anatomy\_Disease      | 0.869 | 0.864 | 0.867 |Reason\_Disease       | 0.769 | 0.571 | 0.656 |
Method\_Drug          | 0.833 | 0.854 | 0.843 |Test\_Disease         | 0.648 | 0.636 | 0.642 |	
Test\_Items\_Disease  | 0.833 | 0.833 | 0.833 |Pathogenesis\_Disease | 0.486 | 0.692 | 0.571 |
Treatment\_Disease    | 0.771 | 0.877 | 0.821 |Operation\_Disese     | 0.6   | 0.231 | 0.333 |
Amount\_Drug          | 0.850 | 0.791 | 0.819 |
total                 |0.839  |0.837  |0.836  |


## Citation

If you use DiaKG in your research, please cite our [paper](https://arxiv.org/abs/2105.15033):
```
@article{chang2021diakg,
      title={DiaKG: an Annotated Diabetes Dataset for Medical Knowledge Graph Construction}, 
      author={Dejie Chang and Mosha Chen and Chaozhen Liu and Liping Liu and Dongdong Li and Wei Li and Fei Kong and Bangchang Liu and Xiaobin Luo and Ji Qi and Qiao Jin and Bin Xu},
      journal={arXiv preprint arXiv:2105.15033}，
      year={2021}
  }
```
